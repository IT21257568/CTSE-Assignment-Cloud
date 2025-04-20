import uuid
import datetime
from dataclasses import dataclass, field
from typing import Optional, Dict, Any

@dataclass
class Service:
    SERVICE_CODE: str
    SERVICE_NAME: str
    DESCRIPTION: Optional[str] = None
    PRICE: float = 0.0
    UUID: str = field(default_factory=lambda: str(uuid.uuid4()))
    CREATED_USER_CODE: Optional[str] = None
    CREATED_DATE: datetime.datetime = field(default_factory=datetime.datetime.utcnow)
    LAST_MOD_USER_CODE: Optional[str] = None
    LAST_MOD_DATE: Optional[datetime.datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert this Service into a dict suitable for mongo.db.services.insert_one(...)
        """
        doc: Dict[str, Any] = {
            "SERVICE_CODE":       self.SERVICE_CODE,
            "SERVICE_NAME":       self.SERVICE_NAME,
            "DESCRIPTION":        self.DESCRIPTION,
            "PRICE":              self.PRICE,
            "UUID":               self.UUID,
            "CREATED_USER_CODE":  self.CREATED_USER_CODE,
            "CREATED_DATE":       self.CREATED_DATE,
            "LAST_MOD_USER_CODE": self.LAST_MOD_USER_CODE,
        }
        if self.LAST_MOD_DATE:
            doc["LAST_MOD_DATE"] = self.LAST_MOD_DATE
        return doc
