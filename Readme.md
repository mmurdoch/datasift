1. Install Python 2.7.x
2. Run `pip install requests`
3. Run `python characters.py <public_key> <private_key>` (where `<public_key>`
  and `private_key` are your Marvel developer keys -
  (see here for details)[http://developer.marvel.com/signup]

The output is stored into the file `characters.csv` in the current directory
the data fields in this file are:

* The character name
* The unique identifier of the character
* The description of the character (if available)
* The number of comics in which the character has appeared
* The number of stories in which the character has appeared

# Get interaction data from DataSift relating to Marvel

The output is stored into the file `sifted.csv` in the current directory
the data fields in this file are:

* Unique identifier of the event (interaction.id)
* When the event occurred (interaction.created_at)
* Characters mentioned (list of characters found in interaction.hashtags and interaction.content)
* Username of the person who did the mention (interaction.author.username)
* Real name of the person who did the mention (interaction.author.name)
* Gender of the person who did the mention (demographic.gender)
* Number of reblogs (tumblr.meta.reblogged_global)
* Number of likes (tumblr.meta.likes_global)

1. Run `pip install datasift`

# Driving Question
Marvel wants to serve its customers better. To achieve this they want to
understand which of their well known characters are most popular and to
check whether the number of comics and stories available for those characters
is in-line with this popularity.

# Feeds
* Tumblr

# Augmentations
* Interaction
* Language Detection
* Gender
* Links
* Sentiment
* Salience Entities
* Klout

# Notes
Initially I tried to get data for all Marvel characters but this resulted in
500 (Internal Server Errors) being returned by the Marvel API. This occurred
when requesting around the sixth chunk of 100 characters. Requesting lower
numbers of characters per page produced timeouts. Adjusting the code to retry
from where it left off simply caused the server to fail sooner.

So instead I requested details of a specific set of popular Marvel characters.
This also suffered from timeouts but with logic allowing the code to restart
I was able to obtain a set of data to work with.

# Stopping DataSift Python Client Cleanly
There does not currently seem to be a way to cleanly stop the DataSift Python
client cleanly. Ctrl+C causes it to throw KeyboardInterrupt exceptions even
if handled in the calling code. The DataSift library uses twisted calling
`reactor.run()` in `client.py` but contains no code to call `reactor.stop()`.On
non-Windows platforms the DataSift library uses Python multiprocessing.
