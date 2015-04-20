from __future__ import print_function
import hashlib
import json
import os
import re
import requests
import uuid


class TimeoutError(Exception):
    def __str__(self):
        return 'Request timed out'


class ResponseError(Exception):
    def __init__(self, status_code, reason):
        self._status_code = status_code
        self._reason = reason

    def __str__(self):
        return 'Error received: {0} ({1})'.format(
            self._reason, self._status_code)


class CharacterRetriever(object):
    CHARACTERS_FILE_PREFIX = 'characters-'
    CHARACTERS_URI = 'http://gateway.marvel.com:80/v1/public/characters'
    LIMIT = 100
    TIMEOUT_SECONDS = 10
    RETRIES = 3

    """
    Retrieves details of marvel characters via the Marvel API.
    """
    def __init__(self, public_key, private_key):
        self._public_key = public_key
        self._private_key = private_key

    # TODO Test this
    def _create_hash(self, request_id):
        md5 = hashlib.md5()
        md5.update(request_id)
        md5.update(self._private_key)
        md5.update(self._public_key)
        return md5.hexdigest()

    def _get_next_offset(self, filename):
        match = re.match(self.CHARACTERS_FILE_PREFIX +'\d+-(\d+)$', filename)
        if match:
            return int(match.group(1)) + 1

        return None

    def _is_character_file(self, filename):
        return filename.startswith(self.CHARACTERS_FILE_PREFIX)

    def _open_character_file(self, start_offset, end_offset):
        characters_filename = '{0}{1}-{2}'.format(
            self.CHARACTERS_FILE_PREFIX, start_offset, end_offset)
        return open(characters_filename, 'w')

    def _extract_character(self, result):
        return {
            'name': result['name'],
            'id': result['id'],
            'description': result['description'],
            'comic-count': result['comics']['available'],
            'story-count': result['stories']['available']
        }

    def _get_characters(self, get_function, offset):
        request_id = str(uuid.uuid4())
        hash = self._create_hash(request_id)

        parameters = {
            'apikey': self._public_key, 'ts': request_id, 'hash': hash,
            'offset': offset, 'limit': self.LIMIT }

        response = None

        # TODO Add proper retry logic
        try:
            response = get_function(
                self.CHARACTERS_URI, params = parameters,
                timeout = self.TIMEOUT_SECONDS)
        except requests.exceptions.Timeout:
            raise TimeoutError()

        status_code = response.status_code
        if status_code != 200:
            raise ResponseError(status_code, response.reason)

        return response


    def run(self):
        offset = 0

        characters_filenames = filter(self._is_character_file, os.listdir('.'))
        if characters_filenames:
            offsets = map(self._get_next_offset, characters_filenames)
            offset = reduce(max, offsets)

        characters_to_get = True
        while characters_to_get:
            print('Retrieving characters {0} to {1}'.format(
                offset, offset+self.LIMIT-1))

            response = self._get_characters(requests.get, offset)

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

            with self._open_character_file(
                offset, next_offset-1) as character_file:
                characters = [self._extract_character(r) for r in results]
                character_file.write(json.dumps(characters))

            offset = next_offset

            if offset >= total:
                characters_to_get = False
                expected_final_count = total % self.LIMIT
                if expected_final_count != count:
                    print('Warning: expected {0} characters but received {1}'.format(
                        expected_final_count, count))
