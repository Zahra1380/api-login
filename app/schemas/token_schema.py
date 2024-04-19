from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from api import JWT_SECRET_KEY, ALGORITHM, ACCESS_EXPIRES, REFRESH_EXPIRES
from datetime import timedelta


class Settings(BaseModel):
    authjwt_algorithm: str = ALGORITHM
    authjwt_secret_key: str = JWT_SECRET_KEY
    authjwt_denylist_enabled: bool = True
    authjwt_denylist_token_checks: set = {"access","refresh"}
    access_expires: int = ACCESS_EXPIRES
    refresh_expires: int = REFRESH_EXPIRES



