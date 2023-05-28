from dataclasses import dataclass
from typing import Any, Type, TypeVar

from pydantic import BaseModel, EmailStr, Field

from config.database import FirestoreClient

T = TypeVar('T', bound='User')


@dataclass
class User:
    name: str
    email: str
    user_id: str

    @classmethod
    def get_user_from_verified_token(cls: Type[T], token: dict[str, Any]) -> T:
        return cls(name=token['name'], email=token['email'], user_id=token['user_id'])

    def __post_init__(self):
        self.firestore = FirestoreClient().client

    def save(self):
        self.firestore.collection('users').document(
            self.user_id).set({'name': self.name, 'email': self.email})


class GetCurrentUserResponse(BaseModel):
    name: str
    email: str
    user_id: str
