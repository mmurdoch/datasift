from __future__ import print_function
from bson.objectid import ObjectId
from flask import Flask, request, url_for, abort, jsonify, make_response
from pymongo import MongoClient, ASCENDING
from pymongo.errors import DuplicateKeyError

client = MongoClient()

db = client.marvel
interactions = db.interactions

interactions.create_index([('id', ASCENDING)], unique=True)

api = Flask(__name__)

def remove_mongodb_id(interaction):
    interaction.pop('_id')
    return interaction

def remove_mongodb_ids(all_interactions):
    all_interactions = list(all_interactions)

    return [remove_mongodb_id(i) for i in all_interactions]

@api.route('/marvel/api/v1.0/interactions', methods=['GET'])
def get_interactions():
    all_interactions = remove_mongodb_ids(interactions.find())

    return jsonify({'interactions': all_interactions}), 200

@api.route('/marvel/api/v1.0/interactions/<id>', methods=['GET'])
def get_interaction(id):
    interaction = remove_mongodb_id(interactions.find_one({'id': int(id)}))

    return jsonify(interaction), 200

def create_error(message):
    return jsonify({'error': message}), 400

def create_missing_field_error(field_name):
    return create_error('Missing interaction field: {0}'.format(field_name))


class MissingFieldError(Exception):
    def __init__(self, field_name):
        self._error_response = create_missing_field_error(field_name)

    @property
    def error_response(self):
        return self._error_response


def get_field(request, field_name):
    if not field_name in request.json:
       raise MissingFieldError(field_name)

    return request.json[field_name]

@api.route('/marvel/api/v1.0/interactions', methods=['POST'])
def create_interaction():
    if not request.json:
        return create_error('Missing interaction JSON')

    id_field = 'id'
    names_field = 'names'
    sentiment_field = 'sentiment'
    try:
        id = get_field(request, id_field)
        names = get_field(request, names_field)
        sentiment = get_field(request, sentiment_field)
    except MissingFieldError as e:
        return e.error_response

    interaction = {
        id_field: id,
        names_field: names,
        sentiment_field: sentiment
    }

    try:
        interactions.insert(interaction)
    except DuplicateKeyError:
        return jsonify({'error': 'Interaction with id {0} already exists'.format(id)}), 409

    interaction_uri = url_for('get_interaction', id=interaction['id'], _external=True)

    response = make_response(jsonify(remove_mongodb_id(interaction)), 201)
    response.headers['Location'] = interaction_uri

    return response

if __name__ == '__main__':
    api.run(debug=True)
