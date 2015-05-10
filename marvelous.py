from __future__ import print_function
import codecs
import csv
import datasift
import glob
import hashlib
import json
import os
import pickle
import re
import requests
import uuid


CHARACTERS_FILE = 'characters.csv'
INTERACTIONS_DIR = 'interactions'
INTERACTION_EXT = '.int'


class TimeoutError(Exception):
    def __init__(self, timeout_seconds):
        self._timeout_seconds = timeout_seconds

    def __str__(self):
        return 'Request timed out after {0} seconds'.format(
            self._timeout_seconds)


class ResponseError(Exception):
    def __init__(self, status_code, reason):
        self._status_code = status_code
        self._reason = reason

    def __str__(self):
        return 'Received error: {0} ({1})'.format(
            self._reason, self._status_code)


class CharacterRetriever(object):
    CHARACTERS_URI = 'http://gateway.marvel.com:80/v1/public/characters'
    LIMIT = 100
    TIMEOUT_SECONDS = 10

    def __init__(self, public_key, private_key):
        """
        Retrieves details of marvel characters via the Marvel API.

        :param string public_key: Your Marvel API public key
        :param string private_key: Your Marvel API private key
        """
        self._public_key = public_key
        self._private_key = private_key

        if os.path.isfile(CHARACTERS_FILE):
            os.remove(CHARACTERS_FILE)

    def _create_hash(self, request_id):
        md5 = hashlib.md5()
        md5.update(request_id)
        md5.update(self._private_key)
        md5.update(self._public_key)
        return md5.hexdigest()

    def _open_character_file(self):
        return codecs.open(CHARACTERS_FILE, 'a', 'utf-8')

    def _extract_character(self, result):
        return [
            # Prevent non-ASCII characters from preventing CSV storage
            result['name'].encode('ascii', 'ignore'),
            result['id'],
            result['description'].encode('ascii', 'ignore'),
            result['comics']['available'],
            result['stories']['available']
        ]

    def _get_characters(self, get_function, offset):
        request_id = str(uuid.uuid4())
        hash = self._create_hash(request_id)

        parameters = {
            'apikey': self._public_key, 'ts': request_id, 'hash': hash,
            'offset': offset, 'limit': self.LIMIT }

        response = None

        try:
            response = get_function(
                self.CHARACTERS_URI, params = parameters,
                timeout = self.TIMEOUT_SECONDS)
        except requests.exceptions.Timeout:
            raise TimeoutError(self.TIMEOUT_SECONDS)

        status_code = response.status_code
        if status_code != 200:
            raise ResponseError(status_code, response.reason)

        return response

    def run(self):
        """
        Runs the character retriever, storing the output.
        """
        offset = 0

        characters_to_get = True
        while characters_to_get:
            print('Retrieving characters {0} to {1}'.format(
                offset, offset+self.LIMIT-1))

            try:
                response = self._get_characters(requests.get, offset)
            except TimeoutError as timeout_error:
                print(str(timeout_error))
            except ResponseError as response_error:
                print(str(response_error))

            content_json = response.text
            content = json.loads(content_json)
            data = content['data']
            total = data['total']
            count = data['count']
            results = data['results']
            print('Received {0} results'.format(count))
            if int(count) == 0:
                return None

            next_offset = offset + count

            with self._open_character_file() as character_file:
                csv_writer = csv.writer(character_file)

                for result in results:
                    csv_writer.writerow(self._extract_character(result))

            offset = next_offset

            if offset >= total:
                characters_to_get = False
                expected_final_count = total % self.LIMIT
                if expected_final_count != count:
                    print('Warning: expected {0} characters but received {1}'.format(
                        expected_final_count, count))


class InteractionStreamProcessor(object):
    def __init__(self, username, api_key, summarizer):
        """
        Retrieves interactions via the DataSift API and summarizes them.

        :param string username: Your DataSift username
        :param string api_key: Your DataSift API key
        :param InteractionSummarizer summarizer: The interaction summarizer
        """
        self._username = username
        self._api_key = api_key
        self._summarizer = summarizer

    def _get_filename(self, interaction):
        return '{0}/{1}{2}'.format(
            INTERACTIONS_DIR, interaction['interaction']['id'],
            INTERACTION_EXT)

    def _escape_for_contains_any(self, s):
        return s.replace('\\', '\\\\').replace(',', '\\,').replace('"', '\\"')

    def _get_tags_csdl(self, character_names):
        csdl = ''

        for character_name in character_names:
            csdl += self._get_tag_csdl(character_name)

        return csdl

    def _get_tag_csdl(self, character_name):
        return ('tag "' + character_name + '" '
               '{ interaction.content contains "' + character_name + '"'
               ' OR interaction.hashtags contains "' + character_name + '" } ')

    def _get_csdl(self, character_names):
        names_csv = ','.join(character_names)

        return (self._get_tags_csdl(character_names) +
               'return { interaction.type == "tumblr" AND ' +
               'language.tag == "en" AND ' +
               'interaction.content contains "marvel" AND ' +
               '(interaction.content contains_any "' + names_csv + '" OR' +
               ' interaction.hashtags contains_any "' + names_csv + '") }')

    def process(self):
        """
        Retrieves interactions and passes them to the summarizer.
        """
        character_names = set() # Remove duplicate names (e.g. Jean Grey)

        if not os.path.isfile(CHARACTERS_FILE):
            print('{0} file not found'.format(CHARACTERS_FILE))
            return

        with open('characters.csv', 'r') as characters_file:
            csv_reader = csv.reader(characters_file)
            for row in csv_reader:
                character_name = self._escape_for_contains_any(row[0])
                character_names.add(character_name)

        client = datasift.Client(self._username, self._api_key)

        csdl = self._get_csdl(character_names)
        filter = client.compile(csdl)

        @client.on_delete
        def on_delete(interaction):
            interaction_filename = self._get_filename(interaction)
            if os.path.isfile(interaction_filename):
                os.remove(interaction_filename)

        @client.on_closed
        def on_close(wasClean, code, reason):
            print('Stream subscriber shutting down because {0}'.format(reason))

        @client.on_ds_message
        def on_ds_message(msg):
            print('DS Message {0}'.format(msg))

        @client.on_open
        def on_open():
            print('Connected to DataSift')
            @client.subscribe(filter['hash'])
            def on_interaction(interaction):
                with open(
                    self._get_filename(interaction), 'wb') as interaction_file:
                    pickle.dump(interaction, interaction_file)

                self._summarizer.add_interaction(interaction)

        client.start_stream_subscriber()


class InteractionFileProcessor(object):
    """
    Reads interactions from the file system and summarizes them.

    :param InteractionSummarizer summarizer: The interaction summarizer
    """
    def __init__(self, summarizer):
        self._summarizer = summarizer

    def _get_interaction(self, interaction_filename):
        with open(interaction_filename, 'rb') as interaction_file:
            return pickle.load(interaction_file)

    def process(self):
        """
        Retrieves interactions and passes them to the summarizer.
        """
        interaction_files = glob.glob('{0}/*{1}'.format(
            INTERACTIONS_DIR, INTERACTION_EXT))

        map(lambda f: self._summarizer.add_interaction(
            self._get_interaction(f)), interaction_files)


class InteractionSummarizer(object):
    INTERACTIONS_FILE = 'interactions.csv'

    def __init__(self):
        """
        Summarizes interactions.
        """
        if os.path.isfile(self.INTERACTIONS_FILE):
            os.remove(self.INTERACTIONS_FILE)

    def add_interaction(self, interaction):
        """
        Adds an interaction to be summarized.

        :param interaction interaction: The interaction to add
        """
        id = interaction['interaction']['id']
        character_names = map(
            lambda n: n.encode('ascii'), interaction['interaction']['tags'])
        created_at = interaction['interaction']['created_at']
        who = interaction['interaction']['author']['username']

        # Assume missing likes equals zero
        likes = 0
        if 'likes_global' in interaction['tumblr'].get('meta', {}):
            likes = int(interaction['tumblr']['meta']['likes_global'])

        # Assume missing reblogs equals zero
        reblogs = 0
        if 'reblogged_global' in interaction['tumblr'].get('meta', {}):
            reblogs = int(interaction['tumblr']['meta']['reblogged_global'])

        # Assume missing sentiment is neutral
        sentiment = 0
        if 'content' in interaction.get('salience', {}):
            salience_content = interaction['salience']['content']
            if 'sentiment' in salience_content:
                sentiment = salience_content['sentiment']

        with codecs.open(self.INTERACTIONS_FILE, 'a', 'utf-8') as csv_file:
            csv_writer = csv.writer(csv_file)

            csv_writer.writerow([
                id, character_names, created_at,
                who, likes, reblogs, sentiment])


class CharacterSentimentStatistics(object):
    def __init__(self):
        """
        Calculates character sentiment statistics.
        """
        self._character_sentiments = { }

    def _get_sentiments(self, character_name):
        if character_name in self._character_sentiments:
            return self._character_sentiments[character_name]

        return []

    def _get_count_sentiment(self, character_name):
        sentiments = self._get_sentiments(character_name)

        return len(sentiments)

    def _get_mean_sentiment(self, character_name):
        sentiments = self._get_sentiments(character_name)

        return sum(sentiments) / float(len(sentiments))

    def _get_stddev_sentiment(self, character_name):
        sentiments = self._get_sentiments(character_name)

        mean = self._get_mean_sentiment(character_name)
        sum_of_squares = sum((s-mean)**2 for s in sentiments)

        count = self._get_count_sentiment(character_name)
        if count < 2:
            return 0

        variance = sum_of_squares/(count - 1)
        return variance**0.5

    def _get_min_sentiment(self, character_name):
        sentiments = self._get_sentiments(character_name)

        return min(sentiments)

    def _get_max_sentiment(self, character_name):
        sentiments = self._get_sentiments(character_name)

        return max(sentiments)

    def add_sentiment(self, character_names, sentiment):
        """
        Adds a set of characters and the sentiment expressed towards them.

        :param array[string] character_names: The names of the characters
        :param int sentiment: The sentiment expressed towards the character
        """
        for character_name in character_names:
            if not character_name in self._character_sentiments:
                self._character_sentiments[character_name] = []
            character_sentiment = self._character_sentiments[character_name]
            character_sentiment.append(sentiment)

    def calculate(self):
        """
        Calculates statistics for the added character sentiments.

        :return list: Summary statistics for the interactions. Each row in
        the list corresponds to a single character and contains the following
        keys::
            'name' - the character's name
            'mean' - the mean sentiment towards the character
            'stddev' - the standard deviation of the sentiment towards the character
            'count' - the number of interactions mentioning the character
            'min' - the most negative sentiment towards the character
            'max' - the most positive sentiment towards the character
        """
        summary = []

        for character_name in self._character_sentiments.keys():
            summary.append({'name': character_name,
                'count': self._get_count_sentiment(character_name),
                'mean': self._get_mean_sentiment(character_name),
                'stddev': self._get_stddev_sentiment(character_name),
                'min': self._get_min_sentiment(character_name),
                'max': self._get_max_sentiment(character_name)})

        return summary
