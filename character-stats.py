from __future__ import print_function
from boxplot import BoxPlotData
from boxplot import BoxPlot
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

boxplot_data = BoxPlotData('Character', 'Sentiment')
for stats in character_stats:
    boxplot_data.add_category_statistics(
        stats['name'],
        stats['min'],
        stats['mean'] - stats['stddev'],
        stats['mean'],
        stats['mean'] + stats['stddev'],
        stats['max'],
        stats['count'])

boxplot = BoxPlot(boxplot_data)
print(boxplot.render())
