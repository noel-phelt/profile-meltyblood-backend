from typing import Union

from fastapi import APIRouter, Depends

from models.user import GetCurrentUserResponse, User
from routers import deps

router = APIRouter()


@router.get("/current_user",  response_model=GetCurrentUserResponse)
def current_user(token: dict[str, Union[str, int]] = Depends(deps.get_verified_user)):
    current_user = User.get_user_from_verified_token(token)
    return current_user
