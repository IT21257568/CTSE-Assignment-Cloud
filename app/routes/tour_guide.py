from flask import Blueprint, request, jsonify
from app.types.tour_guide import TourGuide
from flask_pymongo import PyMongo
import datetime

# Blueprint setup
tour_guide_bp = Blueprint('tour_guide', __name__)
mongo: PyMongo = None 

# Setter function for injecting mongo
def set_mongo(mongo_instance: PyMongo):
    global mongo
    mongo = mongo_instance

# Helper to convert MongoDB document to JSON-safe
def serialize(doc):
    doc['_id'] = str(doc['_id'])
    return doc

# CREATE
@tour_guide_bp.route('/', methods=['POST'])
def create_guide():
    data = request.get_json()
    guide = TourGuide(
        GUIDE_CODE=data['GUIDE_CODE'],
        GUIDE_NAME=data['GUIDE_NAME'],
        EMAIL=data['EMAIL'],
        PHONE=data.get('PHONE'),
        LANGUAGE=data.get('LANGUAGE'),
        CREATED_USER_CODE=data.get('CREATED_USER_CODE'),
    )
    mongo.db.tour_guides.insert_one(guide.to_dict())
    return jsonify({"message": "Tour guide created", "GUIDE_CODE": guide.GUIDE_CODE}), 201

# READ ALL
@tour_guide_bp.route('/', methods=['GET'])
def get_all_guides():
    guides = mongo.db.tour_guides.find()
    return jsonify([serialize(g) for g in guides]), 200

# READ ONE
@tour_guide_bp.route('/<guide_code>', methods=['GET'])
def get_guide(guide_code):
    guide = mongo.db.tour_guides.find_one({"GUIDE_CODE": guide_code})
    if not guide:
        return jsonify({"error": "Tour guide not found"}), 404
    return jsonify(serialize(guide)), 200

# UPDATE
@tour_guide_bp.route('/<guide_code>', methods=['PUT'])
def update_guide(guide_code):
    data = request.get_json()
    update_fields = {
        "GUIDE_NAME": data.get("GUIDE_NAME"),
        "EMAIL": data.get("EMAIL"),
        "PHONE": data.get("PHONE"),
        "LANGUAGE": data.get("LANGUAGE"),
        "LAST_MOD_USER_CODE": data.get("LAST_MOD_USER_CODE"),
        "LAST_MOD_DATE": datetime.datetime.utcnow(),
    }
    update_fields = {k: v for k, v in update_fields.items() if v is not None}
    result = mongo.db.tour_guides.update_one(
        {"GUIDE_CODE": guide_code},
        {"$set": update_fields}
    )
    if result.matched_count == 0:
        return jsonify({"error": "Tour guide not found"}), 404
    return jsonify({"message": "Tour guide updated"}), 200

# DELETE
@tour_guide_bp.route('/<guide_code>', methods=['DELETE'])
def delete_guide(guide_code):
    result = mongo.db.tour_guides.delete_one({"GUIDE_CODE": guide_code})
    if result.deleted_count == 0:
        return jsonify({"error": "Tour guide not found"}), 404
    return jsonify({"message": "Tour guide deleted"}), 200
