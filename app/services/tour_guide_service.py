from app.types.tour_guide import TourGuide
import datetime

mongo = None

def set_mongo(mongo_instance):
    global mongo
    mongo = mongo_instance

def create_guide(data):
    guide = TourGuide(
        GUIDE_CODE=data['GUIDE_CODE'],
        GUIDE_NAME=data['GUIDE_NAME'],
        EMAIL=data['EMAIL'],
        PHONE=data.get('PHONE'),
        LANGUAGE=data.get('LANGUAGE'),
        CREATED_USER_CODE=data.get('CREATED_USER_CODE'),
    )
    mongo.db.tour_guides.insert_one(guide.to_dict())
    return guide.GUIDE_CODE

def get_all_guides():
    return list(mongo.db.tour_guides.find())

def get_guide(guide_code):
    return mongo.db.tour_guides.find_one({"GUIDE_CODE": guide_code})

def update_guide(guide_code, data):
    update_fields = {
        "GUIDE_NAME": data.get("GUIDE_NAME"),
        "EMAIL": data.get("EMAIL"),
        "PHONE": data.get("PHONE"),
        "LANGUAGE": data.get("LANGUAGE"),
        "LAST_MOD_USER_CODE": data.get("LAST_MOD_USER_CODE"),
        "LAST_MOD_DATE": datetime.datetime.utcnow(),
    }
    update_fields = {k: v for k, v in update_fields.items() if v is not None}
    result = mongo.db.tour_guides.update_one({"GUIDE_CODE": guide_code}, {"$set": update_fields})
    return result.matched_count > 0

def delete_guide(guide_code):
    result = mongo.db.tour_guides.delete_one({"GUIDE_CODE": guide_code})
    return result.deleted_count > 0
