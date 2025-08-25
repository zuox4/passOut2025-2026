from fastapi import APIRouter
from utils import verify_google_token, create_jwt_token, get_current_user
from schemas.token import TokenData
from fastapi import APIRouter, Depends, HTTPException, Header
from fastapi.security import OAuth2PasswordBearer
from utils import verify_google_token, create_jwt_token, decode_jwt_token
from schemas.token import TokenData
from datetime import datetime, timedelta
from typing import Optional

router = APIRouter(
    prefix="/api/auth",
    tags=['Auth']
)


@router.post("/login")
async def auth_google(token_data: TokenData):
    user_info = await verify_google_token(token_data.token)
    print(user_info)
    # Добавляем срок действия (например, 30 дней)
    expires_delta = timedelta(days=30)
    expire = datetime.utcnow() + expires_delta
    jwt_token = create_jwt_token({
        "sub": user_info["sub"],
        "email": user_info["email"],
        "name": user_info.get("name", ""),
        "picture": user_info["picture"],
        "exp": expire.timestamp()  # Добавляем срок действия
    })
    return {"access_token": jwt_token, "token_type": "bearer"}

async def get_token_header(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=400, detail="Invalid authorization header")
    return authorization[7:]  # Удаляем "Bearer "


@router.post("/verify")
async def verify_token(token: str = Depends(get_token_header)):
    try:
        payload = decode_jwt_token(token)

        # Проверяем наличие обязательных полей
        if not payload.get("exp"):
            raise HTTPException(
                status_code=401,
                detail="Token is missing expiration claim"
            )

        # Проверяем срок действия
        if datetime.utcnow() > datetime.fromtimestamp(payload["exp"]):
            raise HTTPException(
                status_code=401,
                detail="Token has expired"
            )

        return {
            "valid": True,
            "user_id": payload.get("sub"),
            "email": payload.get("email"),

            "expires": datetime.fromtimestamp(payload["exp"]).isoformat()  # Конвертируем в строку
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=f"Token verification failed: {str(e)}"
        )