from __future__ import print_function
import datasift
import sys

client = None

datasift_username = sys.argv[1]
datasift_api_key = sys.argv[2]

client = datasift.Client(datasift_username, datasift_api_key, ssl=False)

csdl = ('interaction.type == "tumblr" AND '
        'language.tag == "en" AND ('
        'interaction.content contains_any "Spider-Man" OR '
        'interaction.hashtags contains_any "Spider-Man")')

filter = client.compile(csdl)

@client.on_delete
def on_delete(interaction):
    print('You must delete this to be compliant with T&Cs: {0}'.format(interaction))

@client.on_closed
def on_close(wasClean, code, reason):
    print('Stream subscriber shutting down because {0}'.format(reason))

@client.on_ds_message
def on_ds_message(message):
    print('DS Message {0}'.format(message))

@client.on_open
def on_open():
    print('Connected to DataSift')
    @client.subscribe(filter['hash'])
    def on_interaction(interaction):
        print('{0} by {1} ({2})'.format(
            interaction['interaction']['id'],
            interaction['interaction']['author']['username'],
            interaction['interaction']['created_at']))
        print('-')
        #print('{0}'.format(interaction))
try:
    client.start_stream_subscriber()
except KeyboardInterrupt:
    print('Handling Ctrl+C')
    sys.exit()
