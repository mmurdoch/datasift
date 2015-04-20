from __future__ import print_function
import codecs
import csv
import hashlib
import json
import os
import re
import requests
import uuid


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
    CHARACTERS_FILE_PREFIX = 'characters-'
    CHARACTERS_URI = 'http://gateway.marvel.com:80/v1/public/characters'
    LIMIT = 100
    TIMEOUT_SECONDS = 10

    """
    Retrieves details of marvel characters via the Marvel API.

    :param string public_key: Your Marvel API public key
    :param string private_key: Your Marvel API private key
    """
    def __init__(self, public_key, private_key):
        self._public_key = public_key
        self._private_key = private_key

    def _create_hash(self, request_id):
        md5 = hashlib.md5()
        md5.update(request_id)
        md5.update(self._private_key)
        md5.update(self._public_key)
        return md5.hexdigest()

    def _is_character_file(self, filename):
        return filename.startswith(self.CHARACTERS_FILE_PREFIX)

    def _open_character_file(self):
        return codecs.open('characters.csv', 'a', 'utf-8')

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


class InteractionReceiver(object):
    """
    Retrieves interactions via the DataSift API.

    :param string username: Your DataSift username
    :param string api_key: Your DataSift API key
    """
    def __init__(self, username, api_key):
        self._username = username
        self._api_key = api_key

    def get_csdl(self, character_names):
        return ''
