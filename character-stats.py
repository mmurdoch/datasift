from __future__ import print_function
from marvelous import CharacterSentimentStatistics
import ast
import csv
import os.path

statistics = CharacterSentimentStatistics()

INTERACTIONS_FILE = 'interactions.csv'

if not os.path.isfile(INTERACTIONS_FILE):
    print('{0} file not found'.format(INTERACTIONS_FILE))
    exit(1)

with open(INTERACTIONS_FILE, 'r') as characters_file:
    csv_reader = csv.reader(characters_file)
    for row in csv_reader:
        character_names = ast.literal_eval(row[1])
        sentiment = int(row[6])

        statistics.add_sentiment(character_names, sentiment)

# Ignore characters with fewer than 30 mentions
#summary = filter(lambda row: row['count'] >= 30, character_stats)

# TODO Add command line arguments for sorting and filtering
character_stats = statistics.calculate()
character_stats_mean_descending = sorted(
    character_stats, key=lambda row: row['name'], reverse=True)

max_name_length = 0
for stat in character_stats:
    max_name_length = max(max_name_length, len(stat['name']))

min_sentiment = 0
for stat in character_stats:
    min_sentiment = min(min_sentiment, stat['min'])

max_sentiment = 0
for stat in character_stats:
    max_sentiment = max(max_sentiment, stat['max'])

def spaces_for_row_title(name, max_title_length):
    return ' ' * (max_title_length - len(name) + 1)

def spaces_for_column_title(title, min_column_value, max_column_value):
    return ' ' * (abs(max_column_value - min_column_value)/2 - len(title)/2)

print('Character' + spaces_for_row_title('Character', max_name_length) +
    spaces_for_column_title('Sentiment', min_sentiment, max_sentiment) +
    'Sentiment')

print(spaces_for_row_title('', max_name_length) +
    '-' * abs(min_sentiment) +
    ' ' + '+' * max_sentiment)

print(spaces_for_row_title('', max_name_length) +
    '' * abs(min_sentiment)

for stat in character_stats:
    print(stat['name'])

#Character                 Sentiment
#           ------------------- +++++++++++++++++++
#           1111111111                   1111111111
#           987654321098765432101234567890123456789
#Spider-Man                 .      -*-     .        (240)
#...
