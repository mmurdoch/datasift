from __future__ import print_function
import datasift
import sys

datasift_username = sys.argv[1]
datasift_api_key = sys.argv[2]

client = datasift.Client(datasift_username, datasift_api_key)

csdl = 'interaction.content contains_any "Calvin Klein, GQ, Adidas"'

filter = client.compile(csdl)

@client.on_delete
def on_delete(interaction):
    print('You must delete this to be compliant with T&Cs: {0}'.format(interaction))

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
        print('Received interaction: {0}'.format(interaction))

client.start_stream_subscriber()
