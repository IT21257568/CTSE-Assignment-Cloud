from flask import Blueprint, request, jsonify
from database import mongo
from bson.objectid import ObjectId
import datetime, uuid

service_bp = Blueprint('service_bp', __name__)

# ─── Create ────────────────────────────────────────────────────────────────
@service_bp.route('/', methods=['POST'])
def add_service():
    data = request.get_json() or {}

    service = {
        "SERVICE_CODE":      data.get("SERVICE_CODE", ""),
        "SERVICE_NAME":      data.get("SERVICE_NAME", ""),
        "DESCRIPTION":       data.get("DESCRIPTION", ""),
        "PRICE":             data.get("PRICE", 0.0),
        "UUID":              data.get("UUID", str(uuid.uuid4())),
        "CREATED_USER_CODE": data.get("CREATED_USER_CODE"),
        "CREATED_DATE":      _parse_date(data.get("CREATED_DATE")),
        "LAST_MOD_USER_CODE": data.get("LAST_MOD_USER_CODE"),
        "LAST_MOD_DATE":     _parse_date(data.get("LAST_MOD_DATE"))
    }

    if not service["SERVICE_CODE"] or not service["SERVICE_NAME"]:
        return jsonify({"error": "Service Code and Service Name are required"}), 400

    try:
        result = mongo.db.services.insert_one(service)
        return jsonify({
            "message": "Service added successfully",
            "inserted_id": str(result.inserted_id)
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ─── Read (all) ────────────────────────────────────────────────────────────
@service_bp.route('/', methods=['GET'])
def get_all_services():
    docs = mongo.db.services.find()
    out = []
    for d in docs:
        d['_id'] = str(d['_id'])
        out.append(d)
    return jsonify(out), 200

# ─── Read (one) ────────────────────────────────────────────────────────────
@service_bp.route('/<service_id>', methods=['GET'])
def get_service(service_id):
    try:
        doc = mongo.db.services.find_one({'_id': ObjectId(service_id)})
        if not doc:
            return jsonify({'error': 'Service not found'}), 404
        doc['_id'] = str(doc['_id'])
        return jsonify(doc), 200

    except Exception:
        return jsonify({'error': 'Invalid service ID format'}), 400

# ─── Update ────────────────────────────────────────────────────────────────
@service_bp.route('/<service_id>', methods=['PUT'])
def edit_service(service_id):
    data = request.get_json() or {}
    update = {}

    for field in ('SERVICE_CODE', 'SERVICE_NAME', 'DESCRIPTION', 'PRICE', 'CREATED_USER_CODE', 'LAST_MOD_USER_CODE', 'UUID'):
        if field in data:
            update[field] = data[field]

    if 'CREATED_DATE' in data:
        cd = _parse_date(data['CREATED_DATE'])
        if cd is None:
            return jsonify({"error": "Invalid CREATED_DATE format"}), 400
        update['CREATED_DATE'] = cd

    if 'LAST_MOD_DATE' in data:
        lm = _parse_date(data['LAST_MOD_DATE'])
        if lm is None:
            return jsonify({"error": "Invalid LAST_MOD_DATE format"}), 400
        update['LAST_MOD_DATE'] = lm

    if not update:
        return jsonify({"error": "No updatable fields provided"}), 400

    try:
        result = mongo.db.services.update_one(
            {'_id': ObjectId(service_id)},
            {'$set': update}
        )
        if result.matched_count == 0:
            return jsonify({'error': 'Service not found'}), 404
        return jsonify({"message": "Service updated successfully"}), 200

    except Exception:
        return jsonify({'error': 'Invalid service ID format'}), 400

# ─── Delete ────────────────────────────────────────────────────────────────
@service_bp.route('/<service_id>', methods=['DELETE'])
def delete_service(service_id):
    try:
        result = mongo.db.services.delete_one({'_id': ObjectId(service_id)})
        if result.deleted_count == 0:
            return jsonify({'error': 'Service not found'}), 404
        return jsonify({"message": "Service deleted successfully"}), 200

    except Exception:
        return jsonify({'error': 'Invalid service ID format'}), 400

# ─── Helpers ───────────────────────────────────────────────────────────────
def _parse_date(date_str):
    """
    Parse an ISO‑format date string into a datetime, or use now() if None.
    Returns None on invalid format.
    """
    if not date_str:
        return datetime.datetime.utcnow()
    try:
        return datetime.datetime.fromisoformat(date_str)
    except ValueError:
        return None
