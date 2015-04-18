from __future__ import print_function
import binascii
import hashlib
import requests
import uuid

def create_hash(timestamp, private_key, public_key):
    md5 = hashlib.md5()
    md5.update(timestamp)
    md5.update(private_key)
    md5.update(public_key)
    return binascii.hexlify(hash.digest())

# TODO Pass these in as parameters
public_key = 'ccb9b8274fc0e807f2cfeebcb5ec3146'
private_key = 'a47e9ea55038927616bbe260e138abe0071bd7df'

# TODO ? Change UUID to timestamp?
timestamp = str(uuid.uuid4())

hash = create_hash(timestamp, private_key, public_key)

characters_response = requests.get(
    'http://gateway.marvel.com:80/v1/public/characters?limit=100&apikey={0}&ts={1}&hash={2}'.format(public_key, timestamp, hash))
print(characters_response.status_code)
# Handle non-200 status codes
print(characters_response.text)
