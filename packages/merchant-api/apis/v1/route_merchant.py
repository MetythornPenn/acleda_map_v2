from typing import List

from apis.v1.route_login import get_current_user
from db.models.user import User
from db.repository.merchant import create_new_merchant
from db.repository.merchant import delete_merchant
from db.repository.merchant import list_merchants
from db.repository.merchant import retreive_merchant
from db.repository.merchant import update_merchant
from db.session import get_db
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from schemas.merchant import CreateMerchant
from schemas.merchant import ShowMerchant
from schemas.merchant import UpdateMerchant
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/merchant", response_model=ShowMerchant, status_code=status.HTTP_201_CREATED)
def create_merchant(
    merchant: CreateMerchant,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    merchant = create_new_merchant(blog=merchant, db=db, author_id=current_user.id)
    return merchant


@router.get("/merchant/{id}", response_model=ShowMerchant)
def get_merchant(id: int, db: Session = Depends(get_db)):
    merchant = retreive_merchant(id=id, db=db)
    if not merchant:
        raise HTTPException(
            detail=f"merchants with ID {id} does not exist.",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return merchant


@router.get("/merchants", response_model=List[ShowMerchant])
def get_all_merchant(db: Session = Depends(get_db)):
    merchants = list_merchants(db=db)
    return merchants


@router.put("/merchants/{id}", response_model=ShowMerchant)
def update_a_merchant(
    id: int,
    merchant: UpdateMerchant,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    merchant = update_merchant(id=id, blog=merchant, author_id=current_user.id, db=db)
    if isinstance(merchant, dict):
        raise HTTPException(
            detail=merchant.get("error"),
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return merchant


@router.delete("/delete/{id}")
def delete_a_merchant(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    message = delete_merchant(id=id, author_id=current_user.id, db=db)
    if message.get("error"):
        raise HTTPException(
            detail=message.get("error"), status_code=status.HTTP_400_BAD_REQUEST
        )
    return {"msg": f"Successfully deleted merchant with id {id}"}
