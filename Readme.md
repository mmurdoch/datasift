# Get character names and related information from Marvel

1. Install Python 2.7.x
2. Run `pip install requests`

1. Run `python characters.py <public_key> <private_key>` (where `<public_key>`
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

1. Run `pip install datasift`

# Driving Question
Marvel wants to serve its customers better. To achieve this they want to
understand which of their well known characters are most popular and to
check whether the number of comics and stories available for those characters
is in-line with this popularity.

# Notes
Initially I tried to get data for all Marvel characters but this resulted in
500 (Internal Server Errors) being returned by the Marvel API. This occurred
when requesting around the sixth chunk of 100 characters. Requesting lower
numbers of characters per page produced timeouts. Adjusting the code to retry
from where it left off simply caused the server to fail sooner.

So instead I requested details of a specific set of popular Marvel characters.
This also suffered from timeouts but with logic allowing the code to restart
I was able to obtain a set of data to work with.
