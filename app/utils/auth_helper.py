from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from passlib.context import CryptContext
import time
from app.adapters.db_adapter import get_user_by_username
from app.errors import UnverifiedPasswordError
from app.models import TokenData
# from app.models import User
from app.settings import APP_SECRET_KEY, ALGORITHM

#region user cred login
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def verify_password(plain_password, hashed_password):
    if pwd_context.verify(plain_password, hashed_password):
        return True
    raise UnverifiedPasswordError()

async def authenticate_user(username: str, password: str):
    user = await get_user_by_username(username)
    await verify_password(password, user.hashed_password)
    return user

async def create_access_token(data: dict, expires_time_in_minutes: int = 15):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_time_in_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, APP_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

#endregion 

#region verify token
class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False
        try:
            decoded_token =  jwt.decode(jwtoken, APP_SECRET_KEY, algorithms=[ALGORITHM])
            if not decoded_token["exp"] >= time.time():
                raise
            JWTBearer.authenticated_username =  decoded_token["username"]
        except:
            decoded_token = None
        if decoded_token:
            isTokenValid = True
        return isTokenValid

#endregion 
