from services import get_db
from fastapi import Depends, APIRouter, status, HTTPException
from sqlalchemy.orm import Session
import services.login_service as login_service
import schemas.user_schema as user_schema
from fastapi_jwt_auth import AuthJWT
from . import redis_conn, ACCESS_EXPIRES, REFRESH_EXPIRES
from schemas import token_schema
import main
 
login_router = APIRouter()


@login_router.post('/login/')
async def login(user:user_schema.UserLogin, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    user = await login_service.authenticate_user(email=user.user_email, password=user.user_passwrod, db=db)

    if user is None or user == False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )


    # Use create_access_token() and create_refresh_token() to create our
    # access and refresh tokens
    access_token = Authorize.create_access_token(subject=str(user.user_id))
    refresh_token = Authorize.create_refresh_token(subject=str(user.user_id))
    return {"access_token": access_token, "refresh_token": refresh_token}


@login_router.delete('/access-revoke/')
def access_revoke(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    # Store the tokens in redis with the value true for revoked.
    # We can also set an expires time on these tokens in redis,
    # so they will get automatically removed after they expired.
    jti = Authorize.get_raw_jwt()['jti']
    print('jtiiiii', jti)
    print('expp', main.settings.access_expires)

    print('redis_conn', redis_conn)
    try:
        redis_conn.delete(jti)
        

    except Exception as e:
        print('error', e)

    return {"detail":"Access token has been revoke"}

# Endpoint for revoking the current users refresh token
@login_router.delete('/refresh-revoke/')
def refresh_revoke(Authorize: AuthJWT = Depends()):
    Authorize.jwt_refresh_token_required()

    jti = Authorize.get_raw_jwt()['jti']
    redis_conn.delete(jti)

    return {"detail":"Refresh token has been revoke"}


@login_router.post('/refresh/')
def refresh(Authorize: AuthJWT = Depends()):
    """
    Refresh token endpoint. This will generate a new access token from
    the refresh token, but will mark that access token as non-fresh,
    as we do not actually verify a password in this endpoint.
    """
    Authorize.jwt_refresh_token_required()

    current_user = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token(subject=current_user,fresh=False)
    return {"access_token": new_access_token}

@login_router.post('/fresh-login/')
async def fresh_login(user:user_schema.UserLogin, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    user = await login_service.authenticate_user(email=user.user_email, password=user.user_passwrod, db=db)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    new_access_token = Authorize.create_access_token(subject=user.username,fresh=True)
    return {"access_token": new_access_token}

# Any valid JWT access token can access this endpoint
@login_router.get('/protected/')
def protected(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    current_user = Authorize.get_jwt_subject()
    return {"user": current_user}

# Only fresh JWT access token can access this endpoint
@login_router.get('/protected-fresh/')
def protected_fresh(Authorize: AuthJWT = Depends()):
    Authorize.fresh_jwt_required()

    current_user = Authorize.get_jwt_subject()
    return {"user": current_user}
