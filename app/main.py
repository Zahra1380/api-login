from fastapi import FastAPI, Request
from api.user_api import user_router
from api.login_api import login_router
from api.profile_api import profile_router
from api import redis_conn

from models import engine
import models.user_profile_model as user_profile_model
import sys
from fastapi.responses import JSONResponse
from fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi_jwt_auth import AuthJWT
from schemas.token_schema import Settings



sys.path.append('./')

user_profile_model.Base.metadata.create_all(bind=engine)

app = FastAPI()

settings = Settings()

# callback to get your configuration
@AuthJWT.load_config
def get_config():
    return settings

@AuthJWT.token_in_denylist_loader
def check_if_token_in_denylist(decrypted_token):
    jti = decrypted_token['jti']
    entry = redis_conn.get(jti)
    return entry and entry == 'true'

@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )




# https://indominusbyte.github.io/fastapi-jwt-auth/usage/revoking/

app.include_router(user_router)
app.include_router(login_router)
app.include_router(profile_router)