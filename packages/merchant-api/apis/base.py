from apis.v1 import route_merchant
from apis.v1 import route_login
from apis.v1 import route_user
from fastapi import APIRouter


api_router = APIRouter()
api_router.include_router(route_user.router, prefix="/api/v1/merchant-service", tags=["users"])
api_router.include_router(route_merchant.router, prefix="/api/v1/merchant-service", tags=["merchant"])
api_router.include_router(route_login.router, prefix="/api/v1/merchant-service", tags=["login"])
