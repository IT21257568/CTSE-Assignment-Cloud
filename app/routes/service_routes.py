# routes/service_routes.py
from flask import Blueprint, request, jsonify
from app.services.service_service import (
    create_service, 
    get_all_services as get_services_list,  # Rename the imported function
    get_service_by_id, 
    update_service, 
    delete_service as remove_service  # Rename the imported function
)

service_bp = Blueprint('service_bp', __name__)

@service_bp.route('/', methods=['POST'])
def add_service():
    data = request.get_json() or {}
    try:
        inserted_id = create_service(data)
        return jsonify({"message": "Service added successfully", "inserted_id": inserted_id}), 201
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@service_bp.route('/', methods=['GET'])
def list_services():  # Renamed from get_all_services
    services = get_services_list()  # Use renamed imported function
    return jsonify(services), 200

@service_bp.route('/<service_id>', methods=['GET'])
def get_service(service_id):
    try:
        service = get_service_by_id(service_id)
        if not service:
            return jsonify({'error': 'Service not found'}), 404
        return jsonify(service), 200
    except Exception:
        return jsonify({'error': 'Invalid service ID format'}), 400

@service_bp.route('/<service_id>', methods=['PUT'])
def edit_service(service_id):
    data = request.get_json() or {}
    try:
        updated = update_service(service_id, data)
        if not updated:
            return jsonify({'error': 'Service not found'}), 404
        return jsonify({"message": "Service updated successfully"}), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception:
        return jsonify({'error': 'Invalid service ID format'}), 400

@service_bp.route('/<service_id>', methods=['DELETE'])
def remove_service_by_id(service_id):  # Renamed from delete_service
    try:
        deleted = remove_service(service_id)  # Use renamed imported function
        if not deleted:
            return jsonify({'error': 'Service not found'}), 404
        return jsonify({"message": "Service deleted successfully"}), 200
    except Exception:
        return jsonify({'error': 'Invalid service ID format'}), 400
