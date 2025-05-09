# app/routes/review_routes.py
from flask import Blueprint, request, jsonify
from database import mongo
from app.types.review import Review
from bson.objectid import ObjectId
import datetime, uuid

review_bp = Blueprint('review_bp', __name__)

# ─── Create ────────────────────────────────────────────────────────────────
@review_bp.route('/', methods=['POST'])
def add_review():
    data = request.get_json() or {}

    review = Review(
        REVIEW_CODE         = data.get("REVIEW_CODE", ""),
        REVIEW_DESCRIPTION  = data.get("REVIEW_DESCRIPTION", ""),
        REVIEW_RATING       = data.get("REVIEW_RATING", ""),
        UUID                = data.get("UUID", str(uuid.uuid4())),
        CREATED_USER_CODE   = data.get("CREATED_USER_CODE"),
        CREATED_DATE        = _parse_date(data.get("CREATED_DATE")),
        LAST_MOD_USER_CODE  = data.get("LAST_MOD_USER_CODE"),
        LAST_MOD_DATE       = _parse_date(data.get("LAST_MOD_DATE"))
    )

    if not review.REVIEW_CODE or not review.REVIEW_DESCRIPTION or not review.REVIEW_RATING:
        return jsonify({
            "error": "REVIEW_CODE, REVIEW_DESCRIPTION and REVIEW_RATING are required"
        }), 400

    try:
        res = mongo.db.reviews.insert_one(review.to_dict())
        return jsonify({
            "message":     "Review added successfully",
            "inserted_id": str(res.inserted_id)
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ─── Read (all) ────────────────────────────────────────────────────────────
@review_bp.route('/', methods=['GET'])
def get_all_reviews():
    docs = mongo.db.reviews.find()
    out  = []
    for d in docs:
        d['_id'] = str(d['_id'])
        out.append(d)
    return jsonify(out), 200


# ─── Read (one) ────────────────────────────────────────────────────────────
@review_bp.route('/<review_id>', methods=['GET'])
def get_review(review_id):
    try:
        doc = mongo.db.reviews.find_one({'_id': ObjectId(review_id)})
        if not doc:
            return jsonify({'error': 'Review not found'}), 404
        doc['_id'] = str(doc['_id'])
        return jsonify(doc), 200

    except Exception:
        return jsonify({'error': 'Invalid review ID format'}), 400


# ─── Update ────────────────────────────────────────────────────────────────
@review_bp.route('/<review_id>', methods=['PUT'])
def edit_review(review_id):
    data = request.get_json() or {}
    update = {}

    # updatable fields
    for field in (
        'REVIEW_CODE', 'REVIEW_DESCRIPTION', 'REVIEW_RATING',
        'CREATED_USER_CODE', 'LAST_MOD_USER_CODE', 'UUID'
    ):
        if field in data:
            update[field] = data[field]

    # date fields
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
        result = mongo.db.reviews.update_one(
            {'_id': ObjectId(review_id)},
            {'$set': update}
        )
        if result.matched_count == 0:
            return jsonify({'error': 'Review not found'}), 404
        return jsonify({"message": "Review updated successfully"}), 200

    except Exception:
        return jsonify({'error': 'Invalid review ID format'}), 400


# ─── Delete ────────────────────────────────────────────────────────────────
@review_bp.route('/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    try:
        result = mongo.db.reviews.delete_one({'_id': ObjectId(review_id)})
        if result.deleted_count == 0:
            return jsonify({'error': 'Review not found'}), 404
        return jsonify({"message": "Review deleted successfully"}), 200

    except Exception:
        return jsonify({'error': 'Invalid review ID format'}), 400


# ─── Helpers ───────────────────────────────────────────────────────────────
def _parse_date(date_str):
    """
    Parse an ISO‑format date string into a datetime (UTC if omitted).
    Returns None on invalid format.
    """
    if not date_str:
        return datetime.datetime.utcnow()
    try:
        return datetime.datetime.fromisoformat(date_str)
    except ValueError:
        return None