from apis.v1 import route_blog
from apis.v1 import route_login
from apis.v1 import route_user
from fastapi import APIRouter


api_router = APIRouter()
api_router.include_router(route_user.router, prefix="/api/v1/blog-service", tags=["users"])
api_router.include_router(route_blog.router, prefix="/api/v1/blog-service", tags=["blogs"])
api_router.include_router(route_login.router, prefix="/api/v1/blog-service", tags=["login"])
