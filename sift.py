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

    summarizer = InteractionFileSummarizer()
    processor = None
    if argument_count == 3:
        datasift_username = sys.argv[1]
        datasift_api_key = sys.argv[2]

        processor = InteractionStreamProcessor(
            datasift_username, datasift_api_key, summarizer)
    else:
        processor = InteractionFileProcessor(summarizer)

    processor.process()


# Note: Ctrl+C causes stack trace due to not being handled in other threads...
except KeyboardInterrupt:
    pass
