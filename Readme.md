# Prerequisites
* Install Python 2.7.x

## Install Python libraries required for the web service clients
1. Run `pip install requests`
2. Run `pip install datasift`

## For the Character Sentiment Statistics Web Service

### Install required Python libraries
1. Run `pip install flask`
2. Run `pip install pymongo`

### Setup MongoDB (for development)
1. Install MongoDB (for example using Homebrew on a Mac by running `brew install mongodb`)
2. Run `mkdir [path_to_data_dir]`
3. Run `echo dbpath=[path_to_data_dir] > mongodb.config`
4. Run `mongod --config mongodb.config`

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

# Character Sentiment Statistics Web Service
## Run the web service

`python marvel-ws.py`

## View the web service API documentation
1. Point your web browser at [http://editor.swagger.io/#/](http://editor.swagger.io/#/)
2. Click File | Import File... and import the  `api-doc.yaml` file
3. The Swagger editor will display the API documentation in your browser

# Upload Interactions to the Web Service
To upload interactions stored in the `interactions` directory by `sift.py` run:

`python marvel-ws-uploader.py`

This stores the interactions into MongoDB so that statistics can be calculated by the web service on request.

# Calculate Character Sentiment Statistics
Run the web service client to request the web service to calculate statistics from the interactions stored in MongoDB.

Running `python marvel-ws-client.py` will output statistics for all characters.

The output can be filtered and sorted via command line arguments. For example, running:

`python marvel-ws-client.py -fcount -ogt -v30 -smean -r`

will reduce the output to only show sentiment statistics for characters appearing in more than 30 interactions and the output will be listed in descending order by the mean value of their sentiment.

You can get more information about the command line arguments by running:

`python marvel-ws-client.py -h`

# Run Unit Tests
Run `python marvelous-test.py` to execute the unit tests.

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
