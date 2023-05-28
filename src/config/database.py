from typing import Any, Type, TypeVar

from fastapi import Depends, HTTPException, status
from firebase_admin import firestore
from pydantic import BaseModel, Field, PrivateAttr

from config.firebase import FireBaseInit


class FirestoreClient:
    def __init__(self):
        Depends(FireBaseInit)
        self.client = firestore.client()