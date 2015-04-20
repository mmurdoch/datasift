# Get character names and related information from Marvel

1. Install Python 2.7.x
2. Run `pip install requests`

# Unit tests
1. Run `python marvelous-test.py` to execute the unit tests

1. Run `python get-characters.py <public_key> <private_key>` (where `<public_key>`
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

1. Run `python sift.py <datasift_username> <datsift_api_key> [record]`

Where `<datasift_username>` and `<datasift_api_key>` are your DataSift
credentials.

To record interactions from DataSift specify `record` as the third argument.
If this is missing, `sift.py` will try to read interactions from files in the
current directory.

# Driving Question
Marvel wants to serve its customers better. To achieve this they want to
understand which of their well known characters are most popular and to
check whether the number of comics and stories available for those characters
is in-line with this popularity.
