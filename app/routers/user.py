from fastapi import APIRouter, HTTPException, status

from app.models.usermodel import NewUser, UserInDB, User
from app.adapters.db_adapter import insert_user
from app.utils.auth_helper import pwd_context


router = APIRouter()

@router.post("/users/")
async def create_user(new_user: NewUser):
    if new_user.role in ["private","buisness"]:
        hashed_password = pwd_context.hash(new_user.password)
        del new_user.password
        insert_user(new_user, hashed_password)
        return [{"item_id": "Foo", "owner": new_user.username}]
    raise HTTPException(status_code=403, detail="User role forbidden") 