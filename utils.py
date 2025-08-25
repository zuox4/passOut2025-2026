import requests
from fastapi import HTTPException, Depends, status
from google.oauth2 import id_token
from google.auth.transport import requests
from jose import JWTError, jwt
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.exc import InvalidTokenError

from schemas.user import User

security = HTTPBearer()
GOOGLE_CLIENT_ID = "371332661481-l286ctjq3ipq9ujg4r3jiqusvbd69c3p.apps.googleusercontent.com"
# SECRET_KEY = "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"
SECRET_KEY = "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"

ALGORITHM = "HS256"


# функция проверки токена в сервисе гугл
async def verify_google_token(token: str):
    print(token)
    idinfo = id_token.verify_oauth2_token(
        token,
        requests.Request(),

    )
    print(idinfo)
    try:
        idinfo = id_token.verify_oauth2_token(
            token,
            requests.Request(),

        )
        print(idinfo)
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError("Неверный издатель токена")

        return idinfo
    except ValueError:
        raise HTTPException(status_code=401, detail="Невалидный токен")


# Генерация JWT
def create_jwt_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Невалидные учетные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Декодируем JWT токен
        payload = jwt.decode(
            credentials.credentials,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        # Проверяем наличие обязательных полей
        user_id = payload.get("sub")
        email = payload.get("email")
        if user_id is None or email is None:
            raise credentials_exception

        return User(
            id=user_id,
            email=email,
            name=payload.get("name", "")
        )
    except JWTError:
        raise credentials_exception

def decode_jwt_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except InvalidTokenError:
        raise InvalidTokenError("Invalid token")