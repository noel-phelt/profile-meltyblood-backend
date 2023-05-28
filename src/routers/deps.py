
from typing import Union

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from firebase_admin import auth

from config.firebase import FireBaseInit


def get_verified_user(cred: HTTPAuthorizationCredentials = Depends(HTTPBearer()), firebase: FireBaseInit = Depends(FireBaseInit)) -> dict[str, Union[str, int]]:
    try:
        decoded_token: dict[
            str, Union[str, int]
        ] = auth.verify_id_token(cred.credentials)
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication credentials. {err}",
            headers={'WWW-Authenticate': 'Bearer error="invalid_token"'},
        )
    user = decoded_token
    return user
