from typing import Union

from fastapi import APIRouter, Depends, HTTPException, Request, status

from models.profile import Profile, ProfileIn
from models.user import User
from routers import deps

router = APIRouter()


@router.get("/profile/{id}", response_model=Profile)
def get_profile(id: str):
    try:
        profile = Profile.get_profile(id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Not found spectified resource',
        )
    return profile


@router.put("/profile")
def update_my_profile(profile_in: ProfileIn = Depends(ProfileIn.as_form),  token: dict[str, Union[str, int]] = Depends(deps.get_verified_user)):

    current_user = User.get_user_from_verified_token(token)
    profile = Profile.create_updated_profile(profile_in, current_user)
    profile.save(current_user)
    return profile
    # return current_user
