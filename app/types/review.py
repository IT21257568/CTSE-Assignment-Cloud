# app/types/booking.py
import uuid
import datetime
from dataclasses import dataclass, field
from typing import Optional, Dict, Any

@dataclass
class Booking:
    REVIEW_CODE: str
    REVIEW_DESCRIPTION: str
    REVIEW_RATING: str
    UUID: str = field(default_factory=lambda: str(uuid.uuid4()))
    CREATED_USER_CODE: Optional[str] = None
    CREATED_DATE: datetime.datetime = field(default_factory=datetime.datetime.utcnow)
    LAST_MOD_USER_CODE: Optional[str] = None
    LAST_MOD_DATE: Optional[datetime.datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert this Booking into a dict suitable for mongo.db.reviews.insert_one(...)
        """
        doc: Dict[str, Any] = {
            "REVIEW_CODE":       self.REVIEW_CODE,
            "REVIEW_DESCRIPTION":       self.REVIEW_DESCRIPTION,
            "REVIEW_RATING":       self.REVIEW_RATING,
            "UUID":               self.UUID,
            "CREATED_USER_CODE":  self.CREATED_USER_CODE,
            "CREATED_DATE":       self.CREATED_DATE,
            "LAST_MOD_USER_CODE": self.LAST_MOD_USER_CODE,
        }
        if self.LAST_MOD_DATE:
            doc["LAST_MOD_DATE"] = self.LAST_MOD_DATE
        return doc