import uuid
import datetime
from dataclasses import dataclass, field
from typing import Optional, Dict, Any

@dataclass
class TourGuide:
    GUIDE_CODE: str
    GUIDE_NAME: str
    EMAIL: str
    PHONE: Optional[str] = None
    LANGUAGE: Optional[str] = None
    UUID: str = field(default_factory=lambda: str(uuid.uuid4()))
    CREATED_USER_CODE: Optional[str] = None
    CREATED_DATE: datetime.datetime = field(default_factory=datetime.datetime.utcnow)
    LAST_MOD_USER_CODE: Optional[str] = None
    LAST_MOD_DATE: Optional[datetime.datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        doc: Dict[str, Any] = {
            "GUIDE_CODE":         self.GUIDE_CODE,
            "GUIDE_NAME":         self.GUIDE_NAME,
            "EMAIL":              self.EMAIL,
            "PHONE":              self.PHONE,
            "LANGUAGE":           self.LANGUAGE,
            "UUID":               self.UUID,
            "CREATED_USER_CODE":  self.CREATED_USER_CODE,
            "CREATED_DATE":       self.CREATED_DATE,
            "LAST_MOD_USER_CODE": self.LAST_MOD_USER_CODE,
        }
        if self.LAST_MOD_DATE:
            doc["LAST_MOD_DATE"] = self.LAST_MOD_DATE
        return doc
