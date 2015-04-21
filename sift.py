from __future__ import print_function
import csv
import datasift
import os
import sys

try:
    if len(sys.argv) < 3:
        print('Usage: python sift.py <datasift_username> <datasift_api_key> [record]')
        exit(0)

    datasift_username = sys.argv[1]
    datasift_api_key = sys.argv[2]

    def create_csdl(character_names):
        return ('interaction.type == "tumblr" AND ' +
               'language.tag == "en" AND ' +
               '(interaction.content contains_any "' + character_names + '" OR' +
               ' interaction.hashtags contains_any "' + character_names + '")')

    recording = False
    if sys.argv[3] == 'record':
        recording = True

    if recording:
        interaction_count = 0

        characters = []
        with open('characters.csv', 'r') as characters_file:
            csv_reader = csv.reader(characters_file)
            for row in csv_reader:
                character_name = row[0].replace('\\', '\\\\').replace(',', '\\,').replace('"', '\\"')
                characters.append(character_name)
        character_names = ','.join(characters)

        client = datasift.Client(datasift_username, datasift_api_key)

        csdl = create_csdl(character_names)
        print(csdl)
        filter = client.compile(csdl)

        def get_filename(interaction):
            return 'interactions/{0}'.format(interaction['interaction']['id'])

        @client.on_delete
        def on_delete(interaction):
            os.remove(get_filename(interaction))

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

                # TODO This is being referenced before being initialized...
                interaction_count += 1
                if interaction_count % 100 == 0:
                    print('Received {0} interactions so far'.format(
                        interaction_count))

                with open(get_filename(interaction), 'wb') as interaction_file:
                    interaction_file.write(str(interaction))

        client.start_stream_subscriber()

# Note: Ctrl+C causes stack trace due to not being handled in other threads...
except KeyboardInterrupt:
    pass
