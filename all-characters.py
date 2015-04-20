from __future__ import print_function
from marvel.marvel import Marvel
import binascii
import codecs
import hashlib
import json
import os
import re
import requests
import requests.exceptions
import sys
import time
import uuid

public_key = sys.argv[1]
private_key = sys.argv[2]

CHARACTERS_FILE_PREFIX = 'characters-'

def open_character_file(start_offset, end_offset):
    characters_filename = '{0}{1}-{2}'.format(
        CHARACTERS_FILE_PREFIX, start_offset, end_offset)
    return codecs.open(characters_filename, 'w', 'utf-8')

def extract_character(result):
    return {
        'name': result.name,
        'id': result.id,
        'description': result.description,
        'comic-count': result.comics.available,
        'story-count': result.stories.available
    }

def is_character_file(filename):
    return filename.startswith(CHARACTERS_FILE_PREFIX)

def extract_offset(filename):
    match = re.match(CHARACTERS_FILE_PREFIX +'\d+-(\d+)$', filename)
    if match:
        return int(match.group(1)) + 1

    print('Error: Found no match for offset in filename {0}'.format(filename))
    exit(1)

CHARACTERS_URI = 'http://gateway.marvel.com:80/v1/public/characters'
LIMIT = 100

offset = 0

characters_filenames = filter(is_character_file, os.listdir('.'))
if characters_filenames:
    offsets = map(extract_offset, characters_filenames)
    offset = reduce(max, offsets)

characters_to_get = True
while characters_to_get:
    print('Getting characters {0} to {1}'.format(offset, offset+LIMIT-1))

    marvel_api = Marvel(sys.argv[1], sys.argv[2])

    characters_response = None
    try:
        characters_response = marvel_api.get_characters(
            orderBy="name,-modified", limit=str(LIMIT), offset=str(offset))
    except requests.exceptions.Timeout:
        print('Error: Timeout waiting for server')
        exit(1)

    status_code = characters_response.code
    if status_code != 200:
        reason = characters_response.status
        print('Error received: {0} ({1})'.format(reason, status_code))
        exit(1)

    data = characters_response.data
    total = data.total
    count = data.count
    results = data.results
    print('Received {0} results'.format(count))
    next_offset = offset + count

    with open_character_file(offset, next_offset-1) as character_file:
        characters = [extract_character(r) for r in results]
        character_file.write(json.dumps(characters))

    offset = next_offset

    if offset >= total:
        characters_to_get = False
        expected_final_count = total % limit
        if expected_final_count != count:
            print('Warning: expected {0} characters but received {1}'.format(
                expected_final_count, count))
