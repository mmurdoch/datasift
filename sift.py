from __future__ import print_function
from marvelous import InteractionSummarizer
from marvelous import InteractionStreamProcessor
from marvelous import InteractionFileProcessor
import csv
import datasift
import json
import os
import sys

try:
    argument_count = len(sys.argv)

    if argument_count == 2 or argument_count > 3:
        print('Usage: python sift.py [<datasift_username> <datasift_api_key>]')
        exit(0)

    summarizer = InteractionSummarizer()
    processor = None
    if argument_count == 3:
        datasift_username = sys.argv[1]
        datasift_api_key = sys.argv[2]

        processor = InteractionStreamProcessor(
            datasift_username, datasift_api_key, summarizer)
    else:
        processor = InteractionFileProcessor(summarizer)

    processor.process()

    # Ignore characters with fewer than 30 mentions and order the summary
    # statistics descending by mean sentiment
    summary = filter(lambda row: row['count'] >= 30, summarizer.summarize())
    summary = sorted(summary, key=lambda row: row['mean'], reverse=True)

    print('\t\t\tSentiment')
    print('Mentions\tMean\t\tStd. Dev.\tName')
    for row in summary:
        print('{0}\t\t{1}\t\t{2}\t\t\t{3}'.format(
            row['count'], round(row['mean'],2), round(row['stddev'],2),
            row['name']))


# Note: Ctrl+C causes stack trace due to not being handled in other threads...
except KeyboardInterrupt:
    pass
