from __future__ import print_function
from bson.objectid import ObjectId
from flask import Flask, request, url_for, abort, jsonify, make_response
from pymongo import MongoClient, ASCENDING
from pymongo.errors import DuplicateKeyError
from marvelous import SummaryExtractor
from marvelous import CharacterSentimentStatistics

class MissingFieldError(Exception):
    def __init__(self, field_name):
        self._error_response = self.create_missing_field_error(field_name)

    def create_missing_field_error(self, field_name):
        return create_error('Missing interaction field: {0}'.format(field_name))

    @property
    def error_response(self):
        return self._error_response


client = MongoClient()

db = client.marvel
interactions = db.interactions

#TODO This is currently incorrectly detecting duplicates...
#interactions.create_index([('id', ASCENDING)], unique=True)

api = Flask(__name__)

def remove_mongodb_id(interaction):
    interaction.pop('_id')
    return interaction

def remove_mongodb_ids(all_interactions):
    all_interactions = list(all_interactions)

    return [remove_mongodb_id(i) for i in all_interactions]

def create_error(message):
    return jsonify({'error': message}), 400

def get_field(request, field_name):
    if not field_name in request.json:
       raise MissingFieldError(field_name)

    return request.json[field_name]

@api.route('/marvel/api/v1.0/interactions', methods=['GET'])
def get_interactions():
    all_interactions = remove_mongodb_ids(interactions.find())

    return jsonify({'interactions': all_interactions}), 200

@api.route('/marvel/api/v1.0/interactions/<id>', methods=['GET'])
def get_interaction(id):
    interaction = remove_mongodb_id(interactions.find_one({'id': int(id)}))

    return jsonify(interaction), 200

@api.route('/marvel/api/v1.0/interactions', methods=['POST'])
def create_interaction():
    if not request.json:
        return create_error('Missing interaction JSON')

    interaction = request.json

    if not 'interaction' in interaction:
        return jsonify({'error': 'Missing interaction field'}), 400

    if not 'id' in interaction['interaction']:
        return jsonify({'error': 'Missing ID field in interaction'}), 400

    id = interaction['interaction']['id']

    try:
        interactions.insert(interaction)
    except DuplicateKeyError:
        return jsonify({'error': 'Interaction with id {0} already exists'.format(id)}), 409

    interaction_uri = url_for('get_interaction', id=id, _external=True)

    response = make_response(jsonify(remove_mongodb_id(interaction)), 201)
    response.headers['Location'] = interaction_uri

    return response

@api.route('/marvel/api/v1.0/statistics', methods=['GET'])
def get_statistics():
    #Bare minimum: Return JSON of all characters with statistics per name
    all_interactions = remove_mongodb_ids(interactions.find())

    summary_extractor = SummaryExtractor()
    summaries = map(summary_extractor.extract_summary, all_interactions)

    statistics = CharacterSentimentStatistics()
    for summary in summaries:
        statistics.add_sentiment(
            summary['character-names'], summary['sentiment'])

    return jsonify({'statistics': statistics.calculate()}), 200


if __name__ == '__main__':
    api.run(debug=True)
