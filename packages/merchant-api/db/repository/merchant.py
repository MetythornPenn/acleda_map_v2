from db.models.merchant import Merchant
from schemas.merchant import CreateMerchant
from schemas.merchant import UpdateMerchant
from sqlalchemy.orm import Session

from math import radians, sin, cos, sqrt, atan2
from sqlalchemy import func
import sys
sys.setrecursionlimit(10000000)



# create new merchant --------------------------------------------|
def create_new_merchant(merchant: CreateMerchant, db: Session):
    try:
        
        if merchant.latitude is None:
            merchant.latitude = 0
        
        if merchant.longitude is None:
            merchant.longitude = 0
        
        if merchant.name is None:
            merchant.name = ""
        
        merchant = Merchant(**merchant.dict())
        
        db.add(merchant)
        db.commit()
        db.refresh(merchant)
        return merchant
    except Exception as e:
        print(f"Error occurred while creating new merchant: {e}")
        return None


# get merchat by ID ----------------------------------------------|
def get_merchant_by_id(id: int, db: Session):
    merchant = db.query(Merchant).filter(Merchant.id == id).first()    
    return merchant
    
    
# get all merchats -----------------------------------------------|
def get_all_merchants(db: Session):
    merchants = db.query(Merchant).all()
    return merchants
    
    
# get all merchants with pagination ------------------------------|
def get_merchants_with_pagination(page: int, per_page: int, db: Session):
    merchants = db.query(Merchant).offset(page).limit(per_page).all()
    return merchants


# get merchant by name of merchant --------------------------------|
def get_merchant_by_name(name: str, db: Session):
    merchant = db.query(Merchant).filter(Merchant.name == name).first()
    return merchant

    
# get merchant by location latitude & longitude ------------------------------------------------|
def get_merchat_by_lat_long(lat: float, long: float, db: Session):
    merchant = db.query(Merchant).filter( Merchant.latitude == lat, Merchant.longitude == long).first()
    return merchant


# get merchat by name, latitude, longitude of merchant
def get_merchant_by_name_lat_log(name: str,lat: float, long: float, db: Session):
    merchant = db.query(Merchant).filter(Merchant.latitude == lat, Merchant.longitude == long, Merchant.name == name).first()
    return merchant 


# get top 10 nearest merchant by latitude, longitude by calculate radius -----------------------|
def get_top10_nearest_merchant(lat: float, long: float, db: Session):
    # Haversine formula to calculate distance between two points
    def haversine(lat1, lon1, lat2, lon2):
        R = 6371.0  # Radius of the earth in kilometers
        dlat = radians(lat2 - lat1)
        dlon = radians(lon2 - lon1)
        a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = R * c  # Distance in kilometers
        return distance
    
    # Calculate the distance between the merchant with the user, ordered by distance
    merchants = db.query(Merchant).order_by(
        func.sqrt((Merchant.latitude - lat) ** 2 + (Merchant.longitude - long) ** 2)
    ).limit(10).all()
    
    # Filter merchants within a certain radius (e.g., 10km)
    radius = 10  # Radius in kilometers
    nearest_merchants = [merchant for merchant in merchants if haversine(lat, long, merchant.latitude, merchant.longitude) <= radius]
    
    return nearest_merchants



# update merchant by id -------------------------------------------------------------|
def update_merchant(id: int, merchant: UpdateMerchant, author_id: int, db: Session):
    merchant_in_db = db.query(Merchant).filter(Merchant.id == id).first()
    if not merchant_in_db:
        return {"error": f"Merchant with id {id} does not exist"}
    if not merchant_in_db.author_id == author_id:
        return {"error": "Only the author can modify the merchant"}
    merchant_in_db.title = merchant.title
    merchant_in_db.content = merchant.content
    db.add(merchant_in_db)
    db.commit()
    return merchant_in_db

# delete merchant by id -------------------------------------------------------------|
def delete_merchant(id: int, author_id: int, db: Session):
    merchant_in_db = db.query(Merchant).filter(Merchant.id == id)
    if not merchant_in_db.first():
        return {"error": f"Could not find merchant with id {id}"}
    if not merchant_in_db.first().author_id == author_id:
        return {"error": "Only the author can delete a merchant"}
    merchant_in_db.delete()
    db.commit()
    return {"msg": f"Deleted merchant with id {id}"}
