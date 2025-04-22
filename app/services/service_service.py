# services/service_service.py
from bson.objectid import ObjectId
from database import mongo
from app.types.service import Service
from app.utils.date_utils import parse_date

def create_service(data):
    service = Service(
        SERVICE_CODE=data.get("SERVICE_CODE", ""),
        SERVICE_NAME=data.get("SERVICE_NAME", ""),
        DESCRIPTION=data.get("DESCRIPTION"),
        PRICE=data.get("PRICE", 0.0),
        CREATED_USER_CODE=data.get("CREATED_USER_CODE"),
        CREATED_DATE=parse_date(data.get("CREATED_DATE")),
        LAST_MOD_USER_CODE=data.get("LAST_MOD_USER_CODE"),
        LAST_MOD_DATE=parse_date(data.get("LAST_MOD_DATE")),
    )

    if not service.SERVICE_CODE or not service.SERVICE_NAME:
        raise ValueError("Service Code and Service Name are required")

    result = mongo.db.services.insert_one(service.to_dict())
    return str(result.inserted_id)

def get_all_services():
    docs = mongo.db.services.find()
    out = []
    for d in docs:
        d['_id'] = str(d['_id'])
        out.append(d)
    return out

def get_service_by_id(service_id):
    doc = mongo.db.services.find_one({'_id': ObjectId(service_id)})
    if doc:
        doc['_id'] = str(doc['_id'])
    return doc

def update_service(service_id, data):
    update = {}

    for field in ('SERVICE_CODE', 'SERVICE_NAME', 'DESCRIPTION', 'PRICE', 'CREATED_USER_CODE', 'LAST_MOD_USER_CODE', 'UUID'):
        if field in data:
            update[field] = data[field]

    if 'CREATED_DATE' in data:
        cd = parse_date(data['CREATED_DATE'])
        if cd is None:
            raise ValueError("Invalid CREATED_DATE format")
        update['CREATED_DATE'] = cd

    if 'LAST_MOD_DATE' in data:
        lm = parse_date(data['LAST_MOD_DATE'])
        if lm is None:
            raise ValueError("Invalid LAST_MOD_DATE format")
        update['LAST_MOD_DATE'] = lm

    if not update:
        raise ValueError("No updatable fields provided")

    result = mongo.db.services.update_one(
        {'_id': ObjectId(service_id)},
        {'$set': update}
    )
    return result.matched_count > 0

def delete_service(service_id):
    result = mongo.db.services.delete_one({'_id': ObjectId(service_id)})
    return result.deleted_count > 0
