from fastapi import APIRouter, Depends, HTTPException, status

from models.share import Share, ShareIn

router = APIRouter()


@router.get("/shares/{share_id}", response_model=Share)
def get_share(share_id: str):
    share = Share.get_share(share_id)
    if not share:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found specified resource",
        )
    return share


@router.post("/shares", response_model=Share, status_code=status.HTTP_201_CREATED)
def create_share(share_in: ShareIn = Depends(ShareIn.as_form)):
    try:
        share = Share.create_shared_profile(share_in)
        share.save()
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(err),
        ) from err
    return share
