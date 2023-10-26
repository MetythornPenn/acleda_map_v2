from typing import List
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm import Session
# import sys
# sys.setrecursionlimit(1000000000)

from db.session import get_db
from db.repository.merchant import (
    create_new_merchant,
    get_all_merchants,
    get_merchant_by_id,
    get_merchat_by_lat_long,
    get_merchant_by_name,
    get_merchant_by_name_lat_log,
    get_top10_nearest_merchant,
    get_merchants_with_pagination
    )

from schemas.merchant import (
    CreateMerchant, 
    ShowMerchant, 
    UpdateMerchant,
    ShowMerchantWithId,
    )



router = APIRouter()



# create new merchant route ------------------------------------------------------------|
@router.post("/merchant", response_model=ShowMerchant, status_code=status.HTTP_201_CREATED)
def create_merchant(
    merchant: CreateMerchant,
    db: Session = Depends(get_db),
):
    created_merchant = create_new_merchant(merchant=merchant, db=db)
    if not created_merchant:
        raise HTTPException(
            detail=f"Merchant could not be created.",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return created_merchant

# get all merchant route ----------------------------------------------------------------|
@router.get("/merchants", response_model=List[ShowMerchant])
def get_all_merchant(db: Session = Depends(get_db)):
    merchants = get_all_merchants(db=db)
    if not merchants:
        raise HTTPException(
            detail=f"No merchants found.",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return merchants

# get merchants with pagination route -----------------------------------------------------|
@router.get("/merchants/pagination", response_model=List[ShowMerchant])
def get_merchants_with_pagination(page: int, per_page: int, db: Session = Depends(get_db)):
    merchants = get_merchants_with_pagination(page=page, per_page=per_page, db=db)
    if not merchants:
        raise HTTPException(
            detail=f"No merchants found for page {page} and per_page {per_page}.",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return merchants

# get merchant by id route -----------------------------------------------------------------|
@router.get("/merchant/{id}", response_model=ShowMerchant)
def get_merchant(id: int, db: Session = Depends(get_db)):
    merchant = get_merchant_by_id(id=id, db=db)
    if not merchant:
        raise HTTPException(
            detail=f"Merchant with ID {id} not found.",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return merchant

# get merchant by name route -------------------------------------------------------------|
@router.get("/merchant/{name}", response_model=ShowMerchant)
def get_merchant_by_name(name: str, db: Session = Depends(get_db)):
    merchant = get_merchant_by_name(name=name, db=db)
    if not merchant:
        raise HTTPException(
            detail=f"Merchant with name {name} not found.",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return merchant

# get merchant by location latitude & longitude route
@router.get("/merchants/{lat}/{long}", response_model=ShowMerchant)
def get_merchant_by_lat_long(lat: float, long: float, db: Session = Depends(get_db)):
    merchant = get_merchat_by_lat_long(lat=lat, long=long, db=db)
    if not merchant:
        raise HTTPException(
            detail=f"Merchant with latitude {lat} and longitude {long} not found.",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return merchant

# get merchant by name, latitude, longitude of route -------------------------------------------------|
@router.get("/merchants/{name}/{lat}/{long}", response_model=ShowMerchant)
def get_merchat_by_name_lat_long(name: str, lat: float, long: float, db: Session = Depends(get_db)):
    merchant = get_merchant_by_name_lat_log(lat=lat, long=long, db=db)
    if not merchant:
        raise HTTPException(
            detail=f"Merchant with name {name}, latitude {lat}, and longitude {long} not found.",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return merchant

# get top 10 nearest merchant by latitude, longitude by calculate radius route ---------------|
@router.get("/merchants/top10/{lat}/{long}", response_model=List[ShowMerchant])
def get_top10_nearest_merchant(lat: float, long: float, db: Session = Depends(get_db)):
    merchants = get_top10_nearest_merchant(lat=lat, long=long, db=db)
    if not merchants:
        raise HTTPException(
            detail=f"No merchants found within 10km of latitude {lat} and longitude {long}.",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return merchants




# @router.put("/merchants/{id}", response_model=ShowMerchant)
# def update_a_merchant(
#     id: int,
#     merchant: UpdateMerchant,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user),
# ):
#     merchant = update_merchant(id=id, blog=merchant, author_id=current_user.id, db=db)
#     if isinstance(merchant, dict):
#         raise HTTPException(
#             detail=merchant.get("error"),
#             status_code=status.HTTP_404_NOT_FOUND,
#         )
#     return merchant


# @router.delete("/delete/{id}")
# def delete_a_merchant(
#     id: int,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user),
# ):
#     message = delete_merchant(id=id, author_id=current_user.id, db=db)
#     if message.get("error"):
#         raise HTTPException(
#             detail=message.get("error"), status_code=status.HTTP_400_BAD_REQUEST
#         )
#     return {"msg": f"Successfully deleted merchant with id {id}"}



