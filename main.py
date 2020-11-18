# 1. Library imports
import json
import sys
import traceback
import uvicorn
import logging
import requests

from fastapi import Depends, FastAPI, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm, HTTPBearer
from fastapi.templating import Jinja2Templates
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import timedelta
from loguru import logger
from bs4 import BeautifulSoup

from app_configurations.logging_setup.custom_logging import CustomizeLogger, LogFileViewer
from controller.authorization.api_token_manager import Token, TokenData, TokenCoreManager
from app_configurations.app_settings import AppSetting
from controller.user.user_data import UserCoreModel, User
from controller.web_scrape_module.web_scrape_handler import WebScrapeHandler

app_settings = AppSetting()
logger = logging.getLogger(__name__)
config_path = app_settings.LOG_CONFIG_JSON_FILE
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
simple_bearer = HTTPBearer()
templates = Jinja2Templates(directory="templates")


def create_app() -> FastAPI:
    app_ini = FastAPI(title='Qoala Web Scrape API-Documentation', debug=False)
    logger_ini = CustomizeLogger.make_logger(config_path)
    app_ini.logger = logger_ini
    return app_ini


app = create_app()


async def get_current_user(token: str = Depends(simple_bearer)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid crentials or session expired",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        logger.info("Inside main.py=>get_current_user")
        token_str = token.credentials
        payload = jwt.decode(token_str, app_settings.SECRET_KEY, algorithms=app_settings.ALGORITHM)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        logger.error(f'main.py=>get_current_user:{sys.exc_info()[2]}/n{traceback.format_exc()} occurred')
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
def index(request: Request):
    logger.info("main.py=>index")
    return templates.TemplateResponse("home/index.html", {"request": request})


@app.get('/log')
def view_log_types(request: Request):
    logger.info("main.py=>view_log_types")
    log_file_vw = LogFileViewer()
    log_file_types = log_file_vw.list_log_file_types()
    context = {'request': request, 'log_file_types': log_file_types}
    return templates.TemplateResponse("log/index.html", context)


@app.get('/log/{log_type_id:int}')
def get_log_details(request: Request, log_type_id: str):
    try:
        print(f"Inside main.py,get_log_details()=>log_type_id:{log_type_id}")
        logger.info("main.py=>get_all_log_files")
        log_file_vw = LogFileViewer()
        file_list_with_path = log_file_vw.get_all_files(log_type_id)
        context = {'request': request, 'file_list_with_path': file_list_with_path}
        return templates.TemplateResponse("log/logfiles.html", context)
    except Exception:
        logger.error(f'main.py=>get_log_details:{sys.exc_info()[2]}/n{traceback.format_exc()} occurred')


@app.get("/log/{file_path:path}")
async def get_file_content(request: Request, file_path: str):
    try:
        log_file_vw = LogFileViewer()
        file_content = log_file_vw.show_file_content(file_path)
        file_content = file_content.splitlines(True)
        print(f"File reading successful:{file_content}")
        context = {'request': request, 'file_content': file_content, 'file_name': file_path}
        return templates.TemplateResponse('log/file_content.html', context)
    except Exception:
        logger.error(f'main.py=>get_log_details:{sys.exc_info()[2]}/n{traceback.format_exc()} occurred')


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


@app.get("/webscrape/test")
def get_web_scrape_test():
    """
    user_agent = app_settings.WEB_SCRAPE_USER_AGENT
    headers = {"user-agent": user_agent}
    site_url = 'https://www.adidas.com/us/promotions'
    req = requests.get(site_url, headers=headers)
    soup = BeautifulSoup(req.text, "html.parser")
    ele_list = soup.find_all('h2', attrs={'class': 'title___1vL99 withhtml___3nraa gl-heading--l'})
    list_obj = [{"tag-data": str(e.text)} for e in ele_list]
    print(f"list_obj:{list_obj}")
    json_res = json.dumps(list_obj)
    print(type(list_obj))
    """
    web_scrape_handler = WebScrapeHandler()
    result = web_scrape_handler.fetch_site_data()
    print(f"result:{result}")
    res = json.dumps(result)
    print(type(result))
    return {'result': res}


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
