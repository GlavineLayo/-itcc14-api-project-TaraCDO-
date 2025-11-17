from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
CORS(app)

client = MongoClient("mongodb://127.0.0.1:27017")
db = client['taracdo']
establishments = db['establishments']

def serialize_est(est):
    est['_id'] = str(est['_id'])
    return est

@app.route('/establishments', methods=['GET'])
def get_establishments():
    all_est = list(establishments.find())
    return jsonify([serialize_est(e) for e in all_est]), 200

@app.route('/establishments', methods=['POST'])
def add_establishment():
    data = request.json
    res = establishments.insert_one(data)
    new_est = establishments.find_one({'_id': res.inserted_id})
    return jsonify(serialize_est(new_est)), 201

@app.route('/establishments/<id>', methods=['GET'])
def get_establishment(id):
    est = establishments.find_one({'_id': ObjectId(id)})
    if est:
        return jsonify(serialize_est(est)), 200
    return jsonify({'error': 'Establishment not found'}), 404

@app.route('/establishments/<id>', methods=['PUT'])
def update_establishment(id):
    data = request.json
    res = establishments.update_one({'_id': ObjectId(id)}, {'$set': data})
    if res.matched_count:
        updated = establishments.find_one({'_id': ObjectId(id)})
        return jsonify(serialize_est(updated)), 200
    return jsonify({'error': 'Establishment not found'}), 404

@app.route('/establishments/<id>', methods=['DELETE'])
def delete_establishment(id):
    res = establishments.delete_one({'_id': ObjectId(id)})
    if res.deleted_count:
        return jsonify({'message': 'Deleted successfully'}), 200
    return jsonify({'error': 'Establishment not found'}), 404

if __name__ == "__main__":
    app.run(debug=True)
