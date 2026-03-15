from datetime import datetime, timedelta, timezone
from typing import Any, Optional
from uuid import uuid4

from fastapi import UploadFile
from pydantic import BaseModel, Extra, Field, PrivateAttr

from config.cloudstorage import CloudStorage
from config.database import FirestoreClient
from config.env import SHARE, SITE
from models.as_form import as_form

collection_name = "shares"


class ShareBase(BaseModel, extra=Extra.allow):
    player_name: Optional[str] = Field(default=None, max_length=20)
    main_character: Optional[int] = Field(default=None, ge=1, le=20)
    communication_tool: Optional[list[int]] = Field(
        default=None, max_items=4
    )
    play_hard: Optional[list[int]] = Field(default=None, max_items=4)
    playtime_weekend: Optional[int] = Field(default=None, ge=1, le=4)
    playtime_holiday: Optional[int] = Field(default=None, ge=1, le=4)
    style1: Optional[int] = Field(default=None, ge=1, le=22)
    style2: Optional[int] = Field(default=None, ge=1, le=22)
    style3: Optional[int] = Field(default=None, ge=1, le=22)
    rank: Optional[int] = Field(default=None, ge=1, le=10)
    history: Optional[int] = Field(default=None, ge=1, le=4)


@as_form
class ShareIn(ShareBase):
    image: UploadFile = Field(...)
    _cloudstorage: CloudStorage = PrivateAttr()

    def __init__(self, **data: Any):
        super().__init__(**data)
        self._cloudstorage = CloudStorage()

    def upload_image(self, share_id: str) -> dict[str, str]:
        if not self.image.content_type or not self.image.content_type.startswith("image/"):
            raise ValueError("Uploaded file must be an image.")
        return self._cloudstorage.upload_share(self.image, share_id)


class Share(ShareBase):
    share_id: str
    image_path: str
    image_url: str
    share_url: Optional[str] = None
    created_at: datetime
    expires_at: datetime
    _firestore: Any = PrivateAttr()

    def __init__(self, **data: Any):
        super().__init__(**data)
        self._firestore = FirestoreClient().client

    def save(self):
        self._firestore.collection(collection_name).document(
            self.share_id
        ).set(self.dict(exclude_none=True))

    @classmethod
    def get_share(cls, share_id: str):
        data_dict = FirestoreClient().client.collection(
            collection_name
        ).document(share_id).get().to_dict()
        if not data_dict:
            return None
        share = cls.parse_obj(data_dict)
        if share.is_expired():
            return None
        return share

    @classmethod
    def create_shared_profile(cls, share_in: ShareIn):
        share_id = uuid4().hex
        image_data = share_in.upload_image(share_id)
        created_at = datetime.now(timezone.utc)
        share = cls.parse_obj(
            {
                **share_in.dict(exclude={"image"}, exclude_none=True),
                "share_id": share_id,
                "image_path": image_data["path"],
                "image_url": image_data["url"],
                "share_url": cls.build_share_url(share_id),
                "created_at": created_at,
                "expires_at": created_at + timedelta(days=SHARE["expiration_days"]),
            }
        )
        return share

    def is_expired(self) -> bool:
        return self.expires_at <= datetime.now(timezone.utc)

    @staticmethod
    def build_share_url(share_id: str) -> Optional[str]:
        site_url = SITE["url"]
        if not site_url:
            return None
        return f"{site_url.rstrip('/')}/share/{share_id}"
