# Prerequisites
1. Install Python 2.7.x
2. Run `pip install requests`
3. Run `pip install datasift`

# Get Characters from Marvel

Run `python get-characters.py <public_key> <private_key>`

Where `<public_key>` and `private_key` are your Marvel developer keys -
  [see here for details](http://developer.marvel.com/signup).

The output is stored into the file `characters.csv` in the current directory.
The columns in this file are:

* The character name
* The unique identifier of the character
* The description of the character (if available)
* The number of comics in which the character has appeared
* The number of stories in which the character has appeared

# Process Character Mentions from DataSift

Run `python sift.py <datasift_username> <datsift_api_key>`

Where `<datasift_username>` and `<datasift_api_key>` are your DataSift
credentials. This will connect to DataSift and, using the character names from `characters.csv`, retreive a stream of interactions
which will be saved to files in the `interactions` directory and summarized into the file `interactions.csv`.

Each interaction is tagged with the list of characters mentioned in either its
'content' or 'hashtags'.

`interactions.csv` will contain:

* the unique identifier of the interaction (`interaction.id`)
* the characters mentioned (`interaction.tags`)
* when the event occurred (`interaction.created_at`)
* who did the mention (`interaction.author.username`)
* the social reach:
  * (`tumblr.meta.likes_global`)
  * (`tumblr.meta.reblogged_global`)
* the sentiment (`salience.content.sentiment`)

Note: Stop interactions from being streamed by using Ctrl+C. This will cause a
stack trace to be printed. Unfortunately
there doesn't currently seem to be a way to stop the DataSift Python client
gracefully. [Issue raised and pull request submitted on GitHub](https://github.com/datasift/datasift-python/pull/55).

# Process Character Mentions from Files

To read interactions from the `interactions` directory saved locally, run:

`python sift.py`.

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
