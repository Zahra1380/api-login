from services import get_db
from fastapi import Depends, APIRouter, status, HTTPException, Header
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
import services.user_service as user_service
import services.login_service as login_service
import schemas.user_schema as user_schema
from typing import List



user_router = APIRouter()
security = HTTPBearer()



@user_router.post('/users/create/')
async def create_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
        db_user = await user_service.get_user_by_email(db, email=user.user_email)
        print(db_user)
        if db_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='user with this email already exist try another one!')
        user = user_service.create_user(db=db, user=user)
        return user

@user_router.put('/users/update/')
async def update_user(user_schema: user_schema.UserUpdate, token: str = Depends(login_service.get_token_header), db:Session = Depends(get_db)):
    user_id = await login_service.get_payload(token=token)
    print(user_id)
    db_user = user_service.get_user(db, user_id=user_id)

    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='the user with this id not exist!')
    user_service.update_user(db=db, user_schema=user_schema, user_model=db_user)
    return user_service.get_user(db, user_id=user_id)

@user_router.get('/users/list/', response_model=List[user_schema.User])
def read_users(db: Session = Depends(get_db)):
    users = user_service.get_users(db=db)
    return users

@user_router.get('/users/detail/')
def read_user(token: str = Depends(login_service.get_token_header), db: Session = Depends(get_db)):

    user_id = login_service.get_payload(token=token)
    db_user = user_service.get_user(db, user_id=user_id)
    if db_user is None:
        return {'message': 'the user with this id not exist or expired!'}
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='the user with this id not exist!')
    return db_user

@user_router.delete('/users/delete/')
async def delete_user(token: str = Depends(login_service.get_token_header), db:Session = Depends(get_db)):
    user_id = await login_service.get_payload(token=token)
    db_user = user_service.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='the user with this id not exist!')
    user_service.delete_user(db=db, user=db_user)
    return {'message': 'user and user\'s profile successfully deleted!'}

@user_router.put('/users/change/password')
async def change_user_password(token: str = Depends(login_service.get_token_header), user_schema: user_schema.UserChangePassword = Depends(), db:Session = Depends(get_db)):
    user_id = login_service.get_payload(token=token)
    db_user = user_service.get_user(db, user_id=user_id)

    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='the user with this id not exist!')

    user = await login_service.authenticate_user(email=db_user.user_email, password=user_schema.user_old_password, db=db)

    if user_schema.user_new_passwrod != user_schema.user_repeate_new_passwrod:
        raise HTTPException(
            status_code=status.HTTP_304_NOT_MODIFIED, detail='your new password with repeate one is not same'
        ) 

    if not user:
        raise HTTPException(
            status_code=401, detail="Invalid Credentials")
    

    return user_service.change_user_password(db=db, user_schema=user_schema, user_model=db_user)

    