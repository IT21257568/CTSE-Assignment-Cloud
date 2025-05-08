from flask import Blueprint, request, jsonify
from app.services import tour_guide_service

tour_guide_bp = Blueprint('tour_guide', __name__)

def set_mongo(mongo_instance):
    tour_guide_service.set_mongo(mongo_instance)

def serialize(doc):
    doc['_id'] = str(doc['_id'])
    return doc

@tour_guide_bp.route('/', methods=['POST'])
def create_guide():
    data = request.get_json()
    guide_code = tour_guide_service.create_guide(data)
    return jsonify({"message": "Tour guide created", "GUIDE_CODE": guide_code}), 201

@tour_guide_bp.route('/', methods=['GET'])
def get_all_guides():
    guides = tour_guide_service.get_all_guides()
    return jsonify([serialize(g) for g in guides]), 200

@tour_guide_bp.route('/<guide_code>', methods=['GET'])
def get_guide(guide_code):
    guide = tour_guide_service.get_guide(guide_code)
    if not guide:
        return jsonify({"error": "Tour guide not found"}), 404
    return jsonify(serialize(guide)), 200

@tour_guide_bp.route('/<guide_code>', methods=['PUT'])
def update_guide(guide_code):
    data = request.get_json()
    success = tour_guide_service.update_guide(guide_code, data)
    if not success:
        return jsonify({"error": "Tour guide not found"}), 404
    return jsonify({"message": "Tour guide updated"}), 200

@tour_guide_bp.route('/<guide_code>', methods=['DELETE'])
def delete_guide(guide_code):
    success = tour_guide_service.delete_guide(guide_code)
    if not success:
        return jsonify({"error": "Tour guide not found"}), 404
    return jsonify({"message": "Tour guide deleted"}), 200
