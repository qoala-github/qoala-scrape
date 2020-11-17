# 1. Library imports
import json

import uvicorn

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, HTTPBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import timedelta
from authorization.apitokenmanager import Token, TokenData, TokenCoreManager
from data_model.userdata import User, UserCoreModel
from app_configurations.app_settings import AppSetting
from pydantic import BaseModel

app_settings = AppSetting()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
simple_bearer = HTTPBearer()

app = FastAPI()


async def get_current_user(token: str = Depends(simple_bearer)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid crentials or session expired",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        token_str = token.credentials
        payload = jwt.decode(token_str, app_settings.SECRET_KEY, algorithms=app_settings.ALGORITHM)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user_obj = UserCoreModel()
    user = user_obj.get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.get('/')
def index():
    return {'message': 'Hello, stranger'}


@app.get('/Get/User/Json')
def get_users_json(current_user: User = Depends(get_current_active_user)):
    users_db = None
    with open(app_settings.USER_REC_SOURCE_FILE) as f:
        users_db = json.load(f)
    return users_db


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user_obj = UserCoreModel()
    user = user_obj.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token_mng = TokenCoreManager()
    access_token_expires = timedelta(minutes=app_settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = token_mng.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.get("/users/password/hashed")
def get_hashed_password(password):
    return {'actual_password': password, 'hashed_password': pwd_context.hash(password)}


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
