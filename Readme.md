# Prerequisites
1. Install Python 2.7.x
2. Run `pip install requests`
3. Run `pip install datasift`

# Driving Question
Marvel wants to serve its customers better. To achieve this they want to
understand which of their characters are most popular.

# Get Characters from Marvel

* Run `python get-characters.py <public_key> <private_key>`

Where `<public_key>` and `private_key` are your Marvel developer keys -
  [see here for details](http://developer.marvel.com/signup).

The output is stored into the file `characters.csv` in the current directory.
The columns in this file are:

* The character name
* The unique identifier of the character
* The description of the character (if available)
* The number of comics in which the character has appeared
* The number of stories in which the character has appeared

# Get Character Mentions from DataSift

Run `python sift.py <datasift_username> <datsift_api_key>`

Where `<datasift_username>` and `<datasift_api_key>` are your DataSift
credentials. This will connect to DataSift and receive a stream of interactions
which will be saved to files in the `interactions` directory and summarized.

Each interaction is tagged with the list of characters mentioned in either its
'content' or 'hashtags'.

Note: Stop interactions from being streamed by using Ctrl+C. This will cause a
stack trace to be printed (and the summary will not be printed). Unfortunately
there doesn't currently seem to be a way to stop the DataSift Python client
gracefully.

# Summarize Character Mentions

Run `python sift.py`

This will read all interactions from the `interactions` directory, summarize
them and print the results.

# Run Unit Tests
Run `python marvelous-test.py` to execute the unit tests

# DataSift Configuration Notes
## Feeds
* Tumblr

## Augmentations
* Interaction
* Language Detection
* Gender
* Links
* Sentiment
* Salience Entities
* Klout

# Stopping DataSift Python Client Cleanly
There does not currently seem to be a way to cleanly stop the DataSift Python
client cleanly. Ctrl+C causes it to throw KeyboardInterrupt exceptions even
if handled in the calling code. The DataSift library uses twisted calling
`reactor.run()` in `client.py` but contains no code to call `reactor.stop()`. [Issue raised]()
