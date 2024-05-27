from dotenv import load_dotenv, dotenv_values
from fastapi.templating import Jinja2Templates
import os


#папка с шаблонами html
templates = Jinja2Templates(directory="src/templates")

# load_dotenv()
config = dotenv_values(".test.env")

#креды для тестовой БД
DB_NAME_TEST=config.get("DB_NAME_TEST")
DB_USER_TEST=config.get("DB_USER_TEST")
DB_PASS_TEST=config.get("DB_PASS_TEST")
DB_HOST_TEST=config.get("DB_HOST_TEST")
DB_PORT_TEST=config.get("DB_PORT_TEST")
MODE=config.get("MODE")



# #для почты
# PORT = os.environ.get("PORT")
# HOST = os.environ.get("HOST")
# HOST_USER = os.environ.get("HOST_USER")
# HOST_PASSWORD = os.environ.get("HOST_PASSWORD")
# DEFAULT_EMAIL = os.environ.get("DEFAULT_EMAIL")

# #ключи для шифрования
# KEY = os.environ.get("KEY")#для jwt access токена при авторизации
# KEY2 = os.environ.get("KEY2")#для рефреш токена
# KEY3 = os.environ.get("KEY3")#для токена активации
# KEY4 = os.environ.get("KEY4")#для токена при сброе пароля

# ALG = os.environ.get("ALGORITHM")

# #время жизни токенов
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



