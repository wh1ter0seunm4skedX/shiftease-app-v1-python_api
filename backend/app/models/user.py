from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class User(BaseModel):
    id: str = Field(..., description="Firebase UID")
    email: str = Field(..., description="User's email address")
    name: str = Field(..., description="User's full name")
    role: str = Field(..., description="User's role (youth_worker or admin)")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None

    class Config:
        json_schema_extra = {
            "example": {
                "id": "firebase_uid_123",
                "email": "user@example.com",
                "name": "John Doe",
                "role": "youth_worker",
                "created_at": "2025-02-11T16:53:34",
                "last_login": "2025-02-11T16:53:34"
            }
        }
