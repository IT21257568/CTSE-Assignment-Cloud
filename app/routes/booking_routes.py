from flask import Blueprint, request, jsonify
from database import mongo
from app.types.booking import Booking

booking_bp = Blueprint('booking_bp', __name__)

@booking_bp.route('/', methods=['POST'])
def add_booking():
    data = request.get_json() or {}

    # build a Booking instance (will auto‑generate UUID/CREATED_DATE if omitted)
    booking = Booking(
        BOOKING_CODE      = data.get("BOOKING_CODE", ""),
        BOOKING_NAME      = data.get("BOOKING_NAME", ""),
        CREATED_USER_CODE = data.get("CREATED_USER_CODE"),
        # optionally you could override UUID / CREATED_DATE by passing them in data...
        LAST_MOD_USER_CODE= data.get("LAST_MOD_USER_CODE"),
        # LAST_MOD_DATE and others will be parsed in your earlier logic if you need
    )

    # validate required fields
    if not booking.BOOKING_CODE or not booking.BOOKING_NAME:
        return jsonify({"error": "Booking Code and Booking Name are required"}), 400

    # insert into Mongo
    try:
        result = mongo.db.bookings.insert_one(booking.to_dict())
        return jsonify({
            "message": "Booking added successfully",
            "inserted_id": str(result.inserted_id)
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
