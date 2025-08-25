from fastapi import APIRouter
from utils import get_current_user
from schemas.user import User
from fastapi import Depends

router = APIRouter(
    prefix="/api",
    tags=['User']
)


@router.get("/user")
async def get_current_user_data(current_user: User = Depends(get_current_user)):

    return {
        "user_id": current_user.id,
        "email": current_user.email,
        "name": current_user.name
    }
