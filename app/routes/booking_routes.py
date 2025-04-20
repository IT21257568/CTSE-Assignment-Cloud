from flask import Blueprint, request, jsonify
from database import mongo
from app.types.booking import Booking
from bson.objectid import ObjectId
import datetime, uuid

booking_bp = Blueprint('booking_bp', __name__)

# ─── Create ────────────────────────────────────────────────────────────────
@booking_bp.route('/', methods=['POST'])
def add_booking():
    data = request.get_json() or {}

    # build a Booking instance (auto‑UUID & CREATED_DATE)
    booking = Booking(
        BOOKING_CODE       = data.get("BOOKING_CODE", ""),
        BOOKING_NAME       = data.get("BOOKING_NAME", ""),
        UUID               = data.get("UUID", str(uuid.uuid4())),
        CREATED_USER_CODE  = data.get("CREATED_USER_CODE"),
        CREATED_DATE       = _parse_date(data.get("CREATED_DATE")),
        LAST_MOD_USER_CODE = data.get("LAST_MOD_USER_CODE"),
        LAST_MOD_DATE      = _parse_date(data.get("LAST_MOD_DATE"))
    )

    if not booking.BOOKING_CODE or not booking.BOOKING_NAME:
        return jsonify({"error": "Booking Code and Booking Name are required"}), 400

    try:
        result = mongo.db.bookings.insert_one(booking.to_dict())
        return jsonify({
            "message":     "Booking added successfully",
            "inserted_id": str(result.inserted_id)
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ─── Read (all) ────────────────────────────────────────────────────────────
@booking_bp.route('/', methods=['GET'])
def get_all_bookings():
    docs = mongo.db.bookings.find()
    out  = []
    for d in docs:
        d['_id'] = str(d['_id'])
        out.append(d)
    return jsonify(out), 200


# ─── Read (one) ────────────────────────────────────────────────────────────
@booking_bp.route('/<booking_id>', methods=['GET'])
def get_booking(booking_id):
    try:
        doc = mongo.db.bookings.find_one({'_id': ObjectId(booking_id)})
        if not doc:
            return jsonify({'error': 'Booking not found'}), 404
        doc['_id'] = str(doc['_id'])
        return jsonify(doc), 200

    except Exception:
        return jsonify({'error': 'Invalid booking ID format'}), 400


# ─── Update ────────────────────────────────────────────────────────────────
@booking_bp.route('/<booking_id>', methods=['PUT'])
def edit_booking(booking_id):
    data = request.get_json() or {}
    update = {}

    # allow updating any of these fields
    for field in ('BOOKING_CODE', 'BOOKING_NAME', 'CREATED_USER_CODE', 'LAST_MOD_USER_CODE', 'UUID'):
        if field in data:
            update[field] = data[field]

    # handle date fields
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
        result = mongo.db.bookings.update_one(
            {'_id': ObjectId(booking_id)},
            {'$set': update}
        )
        if result.matched_count == 0:
            return jsonify({'error': 'Booking not found'}), 404
        return jsonify({"message": "Booking updated successfully"}), 200

    except Exception:
        return jsonify({'error': 'Invalid booking ID format'}), 400


# ─── Delete ────────────────────────────────────────────────────────────────
@booking_bp.route('/<booking_id>', methods=['DELETE'])
def delete_booking(booking_id):
    try:
        result = mongo.db.bookings.delete_one({'_id': ObjectId(booking_id)})
        if result.deleted_count == 0:
            return jsonify({'error': 'Booking not found'}), 404
        return jsonify({"message": "Booking deleted successfully"}), 200

    except Exception:
        return jsonify({'error': 'Invalid booking ID format'}), 400


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
