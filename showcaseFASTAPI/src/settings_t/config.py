from dotenv import load_dotenv, dotenv_values
from fastapi.templating import Jinja2Templates

from pydantic_settings import BaseSettings, SettingsConfigDict
import os


#папка с шаблонами
templates = Jinja2Templates(directory="src/templates")

# load_dotenv()
config = dotenv_values(".test.env")


# DB_HOST=os.environ.get("DB_HOST")
# DB_PORT=os.environ.get("DB_PORT")
# DB_NAME=os.environ.get("DB_NAME")
# DB_USER=os.environ.get("DB_USER")
# DB_PASS=os.environ.get("DB_PASS")
# MODE=os.environ.get("MODE")

DB_HOST=config.get("DB_HOST")
DB_PORT=config.get("DB_PORT")
DB_NAME=config.get("DB_NAME")
DB_USER=config.get("DB_USER")
DB_PASS=config.get("DB_PASS")
MODE=config.get("MODE")
#конфиг верно тенется

# PORT = os.environ.get("PORT")
# HOST = os.environ.get("HOST")
# HOST_USER = os.environ.get("HOST_USER")
# HOST_PASSWORD = os.environ.get("HOST_PASSWORD")
# DEFAULT_EMAIL = os.environ.get("DEFAULT_EMAIL")

# KEY = os.environ.get("KEY")#для jwt access токена при авторизации
# KEY2 = os.environ.get("KEY2")#для рефреш токена
# KEY3 = os.environ.get("KEY3")#для токена активации
# KEY4 = os.environ.get("KEY4")#для токена при сброе пароля

# ALG = os.environ.get("ALGORITHM")

# EXPIRE_TIME = os.environ.get("ACCESS_TOKEN_EXPIRE_TIME")
# EXPIRE_TIME_REFRESH = os.environ.get("REFRESH_TOKEN_EXPIRE_TIME")



# class Settings(BaseSettings):
#     MODE: str
    
#     DB_HOST: str
#     DB_PORT: int
#     DB_USER: str
#     DB_PASS: str
#     DB_NAME: str

#     @property
#     def DB_URL(self):
#         return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

#     model_config = SettingsConfigDict(env_file=".test.env")


# settings = Settings()


