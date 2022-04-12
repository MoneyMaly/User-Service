import uvicorn
from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext

from app.routers import auth, user
from app.consts import DEFAULT_PREFIX, TOKEN_SECTION, USER_SECTION

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()

@app.get('/')
async def index():
  return {'hello': 'world'}

# routers
app.include_router(auth.router, tags=[TOKEN_SECTION])
app.include_router(user.router, prefix=DEFAULT_PREFIX, tags=[USER_SECTION])

if __name__ == '__main__':  # For Debugging
    uvicorn.run(app, host='0.0.0.0', port=5000)