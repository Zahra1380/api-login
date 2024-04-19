from services import get_db
from fastapi import Depends, APIRouter, status, HTTPException
from sqlalchemy.orm import Session
import services.profile_service as profile_service
import schemas.profile_schema as profile_schema
from services import login_service, user_service

profile_router = APIRouter()

    
@profile_router.post('/user/profile/create/', response_model=profile_schema.Profile)
async def create_profile_for_user(
    profile: profile_schema.ProfileCreate,token: str = Depends(login_service.get_token_header), db: Session = Depends(get_db)
):
    
    user_id = await login_service.get_payload(token=token)
    db_user_profile = profile_service.get_user_profile(db=db, user_id=user_id)
    if db_user_profile is None:
        return profile_service.create_user_profile(db=db, profile=profile, user_id=user_id)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='this user already has profile')

@profile_router.put('/users/profile/update/', response_model=profile_schema.Profile)
async def update_user_profile(profile: profile_schema.ProfileUpdate,token: str = Depends(login_service.get_token_header), db: Session = Depends(get_db)):
    user_id = await login_service.get_payload(token=token)
    db_user_profile = profile_service.get_user_profile(db=db, user_id=user_id)
    if db_user_profile is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='The profile with this information does not exist!')
    profile_service.update_user_profile(db=db, profile=profile, user_profile=db_user_profile)
    return profile_service.get_user_profile(db=db, user_id=user_id)

@profile_router.get('/user/profile/detail/', response_model=profile_schema.Profile)
async def read_user_profile(token: str = Depends(login_service.get_token_header), db: Session = Depends(get_db)):
    user_id = await login_service.get_payload(token=token)
    return profile_service.get_user_profile(db=db, user_id=user_id)

@profile_router.delete('/user/profile/delete/')
async def delete_user_profile(token: str = Depends(login_service.get_token_header), db: Session = Depends(get_db)):
    user_id = await login_service.get_payload(token=token)
    db_user_profile = profile_service.get_user_profile(db=db, user_id=user_id)
    if db_user_profile is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='the profile with this information does not exist!')
    profile_service.delete_user_profile(db=db, user_profile=db_user_profile)
    return {'message': f'user\'s profile with id {user_id} successfully deleted!'}