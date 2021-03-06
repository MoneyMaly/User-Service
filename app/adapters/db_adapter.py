import pymongo
from bson import ObjectId

from app.errors import UserNotFoundError, UserAlreadyExistsError
from app.models import UserInDB

client = None
db = None

async def insert_user(new_user, hashed_password):
    user = UserInDB(**dict(new_user))
    user.hashed_password = hashed_password
    user.id = ObjectId()
    try:
        await db.Users.insert_one(user.dict(by_alias=True))
    except pymongo.errors.DuplicateKeyError:
        raise UserAlreadyExistsError(user.username)
    return user

async def get_user_by_username(username: str):
    user = await db['Users'].find_one({'username': username})
    if not user:
        raise UserNotFoundError(username)
    if username == user['username']:
        return UserInDB(**user)
    raise UserNotFoundError(username)   

async def delete_user_by_username(username: str):
    user = await db['Users'].find_one({'username': username})
    if not user:
        raise UserNotFoundError(username)
    if username == user['username']:
        await db['Users'].delete_one({'username': username})
    else:
        raise UserNotFoundError(username)

async def update_users_data(username: str, phone: str, email: str):
    res = await db['Users'].update_one({"username": username},{"$set":{"phone": phone, "email":email}})
    return True 