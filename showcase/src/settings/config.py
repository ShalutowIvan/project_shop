from dotenv import load_dotenv
from fastapi.templating import Jinja2Templates
import os


#папка с шаблонами
templates = Jinja2Templates(directory="src/templates")

load_dotenv()

DB_HOST=os.environ.get("DB_HOST")
DB_PORT=os.environ.get("DB_PORT")
DB_NAME=os.environ.get("DB_NAME")
DB_USER=os.environ.get("DB_USER")
DB_PASS=os.environ.get("DB_PASS")


PORT = os.environ.get("PORT")
HOST = os.environ.get("HOST")
HOST_USER = os.environ.get("HOST_USER")
HOST_PASSWORD = os.environ.get("HOST_PASSWORD")
DEFAULT_EMAIL = os.environ.get("DEFAULT_EMAIL")

KEY = os.environ.get("KEY")#для jwt токена при авторизации
KEY2 = os.environ.get("KEY2")#для сброса пароля и для верификации

ALG = os.environ.get("ALGORITHM")

EXPIRE_TIME = os.environ.get("ACCESS_TOKEN_EXPIRE_TIME")
