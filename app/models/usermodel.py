from typing import Optional
from pydantic import BaseModel, Field

from app.utils.db_helper import PyObjectId

class User(BaseModel):
    username: str
    role: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = False

class UserInDB(User):
    id: Optional[PyObjectId] = Field(alias='_id')
    hashed_password: Optional[str] = None

class NewUser(User):
    password: str 