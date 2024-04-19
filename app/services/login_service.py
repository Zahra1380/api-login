
import models.user_model as user_model
from .user_service import get_user_by_email
from schemas import user_schema
# from jose import jwt
from sqlalchemy.orm import Session
from fastapi import Header, HTTPException, status, Depends
import jwt
from api import JWT_SECRET_KEY, ALGORITHM, redis_conn
from fastapi_jwt_auth import AuthJWT



def check_if_token_in_denylist(decrypted_token):
    jti = decrypted_token['jti']
    entry = redis_conn.get(jti)
    return entry and entry == 'true'


async def authenticate_user(email: str, password: str, db: Session):
    user = await get_user_by_email(email=email, db=db)

    if not user:
        return False
    
    if not user.verify_password(password):
        return False

    return user

def get_token_header(authorize: str = Header(...)):
    if authorize.lower().startswith("bearer: "):
        token = authorize[8:]
        return token

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')

def get_payload(token: str = Depends(get_token_header)):
    payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
    m = check_if_token_in_denylist(payload)
    print(m)
    user_id = payload.get('sub')

    if m is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='token expire')

    
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')
    return int(user_id)
