from typing import Any, Optional, Union

from fastapi import UploadFile
from pydantic import BaseModel, Extra, Field, PrivateAttr

from config.cloudstorage import CloudStorage
from config.database import FirestoreClient
from models.as_form import as_form
from models.user import User

collection_name = 'profiles'


class ProfileBase(BaseModel, extra=Extra.allow):
    player_name: str = Field(default=None, max_length=20)
    main_character: int = Field(default=None, ge=1, le=20)
    communication_tool: list[int] = Field(
        default=None, max_items=4, ge=1, le=4)
    play_hard: list[int] = Field(default=None, max_items=4, ge=1, le=4)
    playtime_weekend: int = Field(default=None,  ge=1, le=4)
    playtime_holiday: int = Field(default=None,  ge=1, le=4)
    style1: int = Field(default=None,  ge=1, le=22)
    style2: int = Field(default=None,  ge=1, le=22)
    style3: int = Field(default=None,  ge=1, le=22)
    rank: int = Field(default=None,  ge=1, le=10)
    history: int = Field(default=None,  ge=1, le=4)


@as_form
class ProfileIn(ProfileBase):
    image: UploadFile = Field(...,)
    _cloudstorage: CloudStorage = PrivateAttr()

    def __init__(self, **data: Any):
        super().__init__(**data)
        self._cloudstorage = CloudStorage()

    def upload_image(self, user: User) -> str:
        file_name = self._cloudstorage.upload_profile(self.image)
        profile = Profile.get_profile(user.user_id)
        if profile:
            self._cloudstorage.delete_profile(profile.image_path)
        return file_name


class Profile(ProfileBase):
    image_path: str
    _firestore: Any = PrivateAttr()

    def __init__(self, **data: Any):
        super().__init__(**data)
        self._firestore = FirestoreClient().client

    def save(self, user: User):
        self._firestore.collection(collection_name).document(
            user.user_id).set(self.dict())

    @classmethod
    def get_profile(cls, id: str):
        data_dict = FirestoreClient().client.collection(
            collection_name).document(id).get().to_dict()
        profile: Union[Profile, None]
        if data_dict:
            profile = cls.parse_obj(data_dict)
        else:
            profile = None

        return profile

    @classmethod
    def create_updated_profile(cls, profile_in: ProfileIn, user: User):
        path = profile_in.upload_image(user)
        profile_base = ProfileBase.parse_obj(
            profile_in.dict(exclude={'image'}))
        setattr(profile_base, "image_path", path)
        profile: Profile = Profile.parse_obj(profile_base)
        return profile
