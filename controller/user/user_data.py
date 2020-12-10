import json
import sys
import traceback
import logging

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, HTTPBearer
from jose import JWTError, jwt
from typing import Optional
from pydantic import BaseModel
from passlib.context import CryptContext
from app_configurations.app_settings import AppSetting
from controller.authorization.api_token_manager import TokenData


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
app_settings = AppSetting()
logger = logging.getLogger(__name__)
simple_bearer = HTTPBearer()
users_db = None
with open(app_settings.USER_REC_SOURCE_FILE) as f:
    users_db = json.load(f)


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):
    hashed_password: str


class UserCoreModel:

    def verify_password(self, plain_password, hashed_password):
        try:
            logger.info("Inside UserCoreModel=>verify_password")
            return pwd_context.verify(plain_password, hashed_password)
        except Exception:
            logger.error(f'UserCoreModel=>verify_password:{sys.exc_info()[2]}/n{traceback.format_exc()} occurred')

    def get_password_hash(self, password):
        try:
            logger.info("Inside UserCoreModel=>get_password_hash")
            return pwd_context.hash(password)
        except Exception:
            logger.error(f'UserCoreModel=>get_password_hash:{sys.exc_info()[2]}/n{traceback.format_exc()} occurred')

    def get_user(self, username: str):
        try:
            logger.info("Inside UserCoreModel=>get_user")
            user_obj = [user_obj for user_obj in users_db if user_obj['username'] == username]
            if user_obj:
                user_dict = user_obj[0]
                return UserInDB(**user_dict)
        except Exception:
            logger.error(f'UserCoreModel=>get_user:{sys.exc_info()[2]}/n{traceback.format_exc()} occurred')

    def authenticate_user(self, username: str, password: str):
        try:
            logger.info("Inside UserCoreModel=>authenticate_user")
            user = self.get_user(username)
            if not user:
                return False
            if not self.verify_password(password, user.hashed_password):
                return False
            return user
        except Exception:
            logger.error(f'UserCoreModel=>authenticate_user:{sys.exc_info()[2]}/n{traceback.format_exc()} occurred')

    async def get_current_user(self, token: str = Depends(simple_bearer)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid crentials or session expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            logger.info("Inside UserCoreModel=>get_current_user")
            token_str = token.credentials
            payload = jwt.decode(token_str, app_settings.SECRET_KEY, algorithms=[app_settings.ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
        except JWTError:
            logger.error(f'UserCoreModel=>get_current_user:{sys.exc_info()[2]}/n{traceback.format_exc()} occurred')
            raise credentials_exception
        user = self.get_user(users_db, username=token_data.username)
        if user is None:
            raise credentials_exception
        return user

    async def get_current_active_user(self, current_user: Depends(get_current_user)):
        try:
            logger.info("Inside UserCoreModel=>get_current_active_user")
            if current_user.disabled:
                raise HTTPException(status_code=400, detail="Inactive user")
            return current_user
        except Exception:
            logger.error(f'UserCoreModel=>get_current_active_user:{sys.exc_info()[2]}/n{traceback.format_exc()} occurred')
