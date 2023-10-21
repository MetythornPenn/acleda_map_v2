from db.models.merchant import Merchant
from schemas.merchant import CreateMerchant
from schemas.merchant import UpdateMerchant
from sqlalchemy.orm import Session


def create_new_merchant(merchant: CreateMerchant, db: Session, author_id: int = 1):
    merchant = Merchant(**merchant.dict(), author_id=author_id)
    db.add(merchant)
    db.commit()
    db.refresh(merchant)
    return merchant


def retreive_merchant(id: int, db: Session):
    merchant = db.query(Merchant).filter(Merchant.id == id).first()
    return merchant


def list_merchants(db: Session):
    merchants = db.query(Merchant).filter(Merchant.is_active == True).all()
    return merchants


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


def delete_merchant(id: int, author_id: int, db: Session):
    merchant_in_db = db.query(Merchant).filter(Merchant.id == id)
    if not merchant_in_db.first():
        return {"error": f"Could not find merchant with id {id}"}
    if not merchant_in_db.first().author_id == author_id:
        return {"error": "Only the author can delete a merchant"}
    merchant_in_db.delete()
    db.commit()
    return {"msg": f"Deleted merchant with id {id}"}
