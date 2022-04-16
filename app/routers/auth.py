from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.errors import UserNotFoundError, UnverifiedPasswordError
from app.models import Token, Message
from app.settings import ACCESS_TOKEN_EXPIRE_MINUTES
from app.utils.auth_helper import authenticate_user, create_access_token

router = APIRouter(tags=['Tokens'])

@router.post("/token", status_code=status.HTTP_200_OK, response_model=Token,
             responses={
                 status.HTTP_401_UNAUTHORIZED: {'model': Message},
                 status.HTTP_404_NOT_FOUND: {'model': Message},
                 status.HTTP_500_INTERNAL_SERVER_ERROR: {'model': Message}
             },
             summary='Generate Access Token', description='Get User Login Access Token')
async def generate_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        user = await authenticate_user(form_data.username, form_data.password)
        access_token = await create_access_token(data={"username": user.username, "role": user.role},
                                                 expires_time_in_minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        return {"access_token": access_token, "token_type": "bearer"}
    except UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except UnverifiedPasswordError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e),
                            headers={"WWW-Authenticate": "Bearer"})
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
