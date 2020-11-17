import json
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, HTTPBearer
from jose import JWTError, jwt
from pydantic import BaseModel
from typing import Optional
from passlib.context import CryptContext
from AppConfigurations.appsettings import AppSetting
from Authorization.apitokenmanager import TokenData

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
appsettings = AppSetting()
simple_bearer = HTTPBearer()
users_db = json.dumps("/DataModel/user.json")

class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

    def verify_password(self, plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password):
        return pwd_context.hash(password)

    def get_user(self, username: str):
        if username in users_db:
            user_dict = users_db[username]
            return UserInDB(**user_dict)

    def authenticate_user(self, username: str, password: str):
        user = self.get_user(users_db, username)
        if not user:
            return False
        if not self.verify_password(password, user.hashed_password):
            return False
        return user

    async def get_current_user(self, token: str = Depends(simple_bearer)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid crentials or session expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            token_str = token.credentials
            payload = jwt.decode(token_str, appsettings, algorithms=[appsettings.ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
        except JWTError:
            raise credentials_exception
        user = self.get_user(users_db, username=token_data.username)
        if user is None:
            raise credentials_exception
        return user

    async def get_current_active_user(self, current_user:Depends(get_current_user)):
        if current_user.disabled:
            raise HTTPException(status_code=400, detail="Inactive user")
        return current_user


class UserInDB(User):
    hashed_password: str
