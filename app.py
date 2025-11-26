from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)
CORS(app)

# --------------------------------
# 🔗 MongoDB Connection
# --------------------------------
client = MongoClient("mongodb://localhost:27017/")  
db = client["taracdo_db"]
collection = db["establishments"]

# Helper function to convert MongoDB documents
def serialize(doc):
    doc["id"] = str(doc["_id"])
    del doc["_id"]
    return doc

# --------------------------------
# 📌 GET ALL ESTABLISHMENTS
# --------------------------------
@app.get("/establishments")
def get_all():
    data = list(collection.find())
    return jsonify([serialize(d) for d in data]), 200

# --------------------------------
# 📌 ADD NEW ESTABLISHMENT
# --------------------------------
@app.post("/establishments")
def add_establishment():
    data = request.json
    result = collection.insert_one(data)
    new_item = collection.find_one({"_id": result.inserted_id})
    return jsonify(serialize(new_item)), 201

# --------------------------------
# 📌 GET ONE BY ID
# --------------------------------
@app.get("/establishments/<id>")
def get_one(id):
    doc = collection.find_one({"_id": ObjectId(id)})
    if doc:
        return jsonify(serialize(doc)), 200
    return jsonify({"error": "Not found"}), 404

# --------------------------------
# 📌 UPDATE ESTABLISHMENT
# --------------------------------
@app.put("/establishments/<id>")
def update(id):
    data = request.json
    updated = collection.update_one({"_id": ObjectId(id)}, {"$set": data})

    if updated.matched_count == 0:
        return jsonify({"error": "Not found"}), 404

    doc = collection.find_one({"_id": ObjectId(id)})
    return jsonify(serialize(doc)), 200

# --------------------------------
# 📌 DELETE ESTABLISHMENT
# --------------------------------
@app.delete("/establishments/<id>")
def delete(id):
    deleted = collection.delete_one({"_id": ObjectId(id)})
    if deleted.deleted_count == 0:
        return jsonify({"error": "Not found"}), 404
    return jsonify({"message": "Deleted"}), 200

# --------------------------------
# RUN SERVER
# --------------------------------
if __name__ == "__main__":
    app.run(debug=True)
