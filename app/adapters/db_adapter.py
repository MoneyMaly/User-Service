from urllib.parse import quote_plus
from pymongo import MongoClient

from app.models.usermodel import User, UserInDB
from app.settings import DATABASE_SERVER, DATABASE_USER, DATABASE_PASSWORD, DATABASE_PORT, DATABASE_NAME

client = MongoClient(host=f'mongodb://{DATABASE_USER}:{quote_plus(DATABASE_PASSWORD)}@{DATABASE_SERVER}:{DATABASE_PORT}/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@moneymaly@')
db = client[DATABASE_NAME]

def put_user(user):
    ret = db.test.insert_one(user.dict(by_alias=True))
    user.id = ret.inserted_id
    return {'user': user}


def get_user(username: str):
    user = db.Users.find_one({"username":username})
    if not user:
        return None
    if username == user['username']:
        return UserInDB(**user)    
