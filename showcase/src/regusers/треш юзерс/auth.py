from fastapi_users.authentication import CookieTransport, AuthenticationBackend
from fastapi_users.authentication import JWTStrategy

from config import KEY, ALG, EXPIRE_SECONDS

cookie_transport = CookieTransport(cookie_name="shop", cookie_max_age=3600)

SECRET_KEY = KEY
ALGORITHM = ALG#алгоритм для подписи jwt токена
ACCESS_TOKEN_EXPIRE_SECONDS = EXPIRE_SECONDS#срок действия токена

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET_KEY, lifetime_seconds=ACCESS_TOKEN_EXPIRE_SECONDS, algorithm=ALGORITHM)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)