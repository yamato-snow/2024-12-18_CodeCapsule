from dataclasses import dataclass
from datetime import datetime
import uuid

@dataclass
class CapsuleData:
    id: str
    code: str
    message: str
    created_at: datetime
    open_at: datetime

    @classmethod
    def create(cls, code: str, message: str, open_at: datetime):
        return cls(
            id=str(uuid.uuid4()),
            code=code,
            message=message,
            created_at=datetime.now(),
            open_at=open_at
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "code": self.code,
            "message": self.message,
            "created_at": self.created_at.isoformat(),
            "open_at": self.open_at.isoformat()
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'CapsuleData':
        return cls(
            id=data["id"],
            code=data["code"],
            message=data["message"],
            created_at=datetime.fromisoformat(data["created_at"]),
            open_at=datetime.fromisoformat(data["open_at"])
        ) 