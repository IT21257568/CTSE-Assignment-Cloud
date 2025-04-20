from flask import Blueprint, jsonify
from database import mongo

test_routes = Blueprint('test_routes', __name__)

@test_routes.route('/test-mongo-connection', methods=['GET'])
def test_mongo_connection():
    try:
        # Attempt to list collections in the database
        collections = mongo.db.list_collection_names()
        return jsonify({"status": "success", "collections": collections}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500