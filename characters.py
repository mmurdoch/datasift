from __future__ import print_function
import binascii
import codecs
import csv
import hashlib
import json
import os
import os.path
import re
import requests
import requests.exceptions
import sys
import uuid

CHARACTER_NAMES = [
    'Daredevil',
    'Hulk',
    'Spider-Man',
    'Iron Man',
    'Professor X',
    'Wolverine',
    'Thor',
    'Cyclops',
    'Magneto',
    'Captain America',
    'Hawkeye',
    'Angel',
    'Beast',
    'Colossus',
    'Emma Frost',
    'Iceman',
    'Jean Grey',
    'Gambit',
    'Nightcrawler',
    'Kitty Pryde',
    'Rogue',
    'Storm',
    'X-23',
    'Juggernaut',
    'Toad',
    'Scarlet Witch',
    'Mystique',
    'Green Goblin',
    'Loki'
]

CHARACTERS_URI = 'http://gateway.marvel.com:80/v1/public/characters'
CHARACTERS_FILENAME = 'characters.csv'
TIMEOUT_SECONDS = 10
RETRIES = 3

def get_last_retrieved_character_name():
    last_character = None

    if character_file_exists():
        with open_character_file_to_read() as character_file:
            csv_reader = csv.reader(character_file)
            for row in csv_reader:
                last_character = row[0]

    return last_character

def remove_retrieved_characters(character_names):
    last_retrieved_character = get_last_retrieved_character_name()
    if last_retrieved_character == None:
        return character_names

    not_retrieved_characters = []

    should_retrieve = False
    for character_name in character_names:
        if should_retrieve:
            not_retrieved_characters.append(character_name)
        elif character_name == last_retrieved_character:
            should_retrieve = True

    return not_retrieved_characters

def character_file_exists():
    return os.path.isfile(CHARACTERS_FILENAME)

def open_character_file(operation):
    return open(CHARACTERS_FILENAME, operation)

def open_character_file_to_read():
    return open_character_file('r')

def open_character_file_to_append():
    return open_character_file('a')

def extract_character(result):
    return [
        result['name'], result['id'], result['description'],
        result['comics']['available'], result['stories']['available']
    ]

def create_hash(request_id, private_key, public_key):
    md5 = hashlib.md5()
    md5.update(request_id)
    md5.update(private_key)
    md5.update(public_key)
    return binascii.hexlify(md5.digest())

def get_id_for_character(character_name):
    request_id = str(uuid.uuid4())
    hash = create_hash(request_id, private_key, public_key)

    parameters = {
        'apikey': public_key, 'ts': request_id, 'hash': hash,
        'limit': 1, 'name': character_name }

    response = None
    try:
        response = requests.get(
            CHARACTERS_URI, params = parameters, timeout = TIMEOUT_SECONDS)
    except requests.exceptions.Timeout:
        print('Error: Timeout waiting for response from {0}, retry later'.format(
            CHARACTERS_URI))
        import time
        time.sleep(10)
        try:
            response = requests.get(
                CHARACTERS_URI, params = parameters, timeout = 10)
        except requests.exceptions.Timeout:
            print('Error: Timeout waiting for response from {0}, retry later'.format(
                CHARACTERS_URI))
            import time
            exit(1)

    status_code = response.status_code
    if status_code != 200:
        reason = response.reason
        print('Error received: {0} ({1})'.format(reason, status_code))
        exit(1)

    content_json = response.text
    content = json.loads(content_json)
    data = content['data']
    count = data['count']
    if int(count) == 0:
        return None
    character_id = data['results'][0]['id']

    return character_id

def retrieve_character_details(character_name):
    print('Getting character {0}'.format(character_name))

    character_id = get_id_for_character(character_name)
    if character_id == None:
        print('Warning: No results received for character {0}, skipping'.format(
            character_name))
        return

    request_id = str(uuid.uuid4())
    hash = create_hash(request_id, private_key, public_key)

    parameters = {
        'apikey': public_key, 'ts': request_id, 'hash': hash }

    response = None
    try:
        uri = '{0}/{1}'.format(CHARACTERS_URI, character_id)
        response = requests.get(uri, params = parameters, timeout = 10)
    except requests.exceptions.Timeout:
        print('Error: Timeout waiting for response from {0}, retry later'.format(uri))
        exit(1)

    status_code = response.status_code
    if status_code != 200:
        reason = response.reason
        print('Error received: {0} ({1})'.format(reason, status_code))
        exit(1)

    content_json = response.text
    content = json.loads(content_json)
    result = content['data']['results'][0]

    with open_character_file_to_append() as character_file:
        csv_writer = csv.writer(character_file)
        csv_writer.writerow(extract_character(result))

public_key = sys.argv[1]
private_key = sys.argv[2]

map(retrieve_character_details, remove_retrieved_characters(CHARACTER_NAMES))
