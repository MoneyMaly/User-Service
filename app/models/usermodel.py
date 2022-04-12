from typing import Optional
from pydantic import BaseModel, Field

from app.utils.db_helper import PyObjectId

class User(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    username: str
    role: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

class UserInDB(User):
    hashed_password: str 