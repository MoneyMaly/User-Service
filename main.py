import uvicorn
from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.routers import auth
from app.consts import DEFAULT_PREFIX, TOKEN_SECTION


app = FastAPI()

@app.get('/')
async def index():
  return {'hello': 'world'}

# routers
app.include_router(auth.router, tags=[TOKEN_SECTION])

if __name__ == '__main__':  # For Debugging
    uvicorn.run(app, host='0.0.0.0', port=5000)