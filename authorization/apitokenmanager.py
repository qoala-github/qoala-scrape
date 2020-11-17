from pydantic import BaseModel
from typing import Optional
from datetime import timedelta, datetime
from jose import JWTError, jwt
from app_configurations.app_settings import AppSetting

app_settings = AppSetting()


class Token(BaseModel):
    access_token: str
    token_type: str

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, app_settings.SECRET_KEY, algorithm=app_settings.ALGORITHM)
        return encoded_jwt


class TokenCoreManager:
    access_token: str
    token_type: str

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, app_settings.SECRET_KEY, algorithm=app_settings.ALGORITHM)
        return encoded_jwt


class TokenData(BaseModel):
    username: Optional[str] = None
