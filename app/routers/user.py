from fastapi import APIRouter, HTTPException, Depends
from starlette import status
from app.adapters.db_adapter import insert_user, get_user_by_username, delete_user_by_username
from app.errors import UserNotFoundError, UserAlreadyExistsError
from app.models import NewUser, UserFromDB, Message, User
from app.utils.auth_helper import pwd_context, JWTBearer
from app.utils.db_helper import to_jsonable_dict

router = APIRouter(tags=['Users'])
@router.post("/users", status_code=status.HTTP_201_CREATED,
             response_model=UserFromDB, response_model_exclude=['hashed_password'],
             responses={
                 status.HTTP_400_BAD_REQUEST: {'model': Message},
                 status.HTTP_409_CONFLICT: {'model': Message},
                 status.HTTP_500_INTERNAL_SERVER_ERROR: {'model': Message}
             },
             summary='Create New User', description='Create New User, user role can be private or business')

async def create_user(new_user: NewUser):
    if new_user.role not in ["private", "business"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User role is not valid")
    try:
        hashed_password = pwd_context.hash(new_user.password)
        del new_user.password
        inserted_user = await insert_user(new_user, hashed_password)
        return to_jsonable_dict(inserted_user.dict(by_alias=True))
    except UserAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/users", status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())],
            response_model=UserFromDB, response_model_exclude=['hashed_password'],
            responses={
                status.HTTP_404_NOT_FOUND: {'model': Message},
                status.HTTP_500_INTERNAL_SERVER_ERROR: {'model': Message}
            },
            summary='Get User', description='Get User by username or by id')

async def get_user(username: str):
    try:
        user = await get_user_by_username(username)
        return to_jsonable_dict(user.dict(by_alias=True))
    except UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.delete("/users", status_code=status.HTTP_200_OK,
               response_model=Message,
               responses={
                   status.HTTP_404_NOT_FOUND: {'model': Message},
                   status.HTTP_500_INTERNAL_SERVER_ERROR: {'model': Message}
               },
               summary='Get User', description='Get User by username or by id')
async def delete_user(username: str):
    try:
        await delete_user_by_username(username)
        return Message(detail=f'User {username} Successfully Deleted')
    except UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
