from fastapi import status
from pydantic import BaseModel


class ErrorResponse(BaseModel):
    detail: str


responses = {
    status.HTTP_200_OK: {"description": "正常"},
    status.HTTP_403_FORBIDDEN: {"description": "権限不正"},
    status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "システムエラー"},
    "default": {"model": ErrorResponse, "description": "その他のエラー"}
}
