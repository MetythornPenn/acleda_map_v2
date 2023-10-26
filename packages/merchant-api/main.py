import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from core.config import settings
from db.base import Base
from db.session import engine
from apis.base import api_router
# def create_tables():
#     Base.metadata.create_all(bind=engine)

# ------------- Router  ------------------
def include_router(app):
    app.include_router(api_router)


# ------------- CORS Middleware ------------------
def middleware(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app

# ------------- Application ------------------
def start_application():
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    # create_tables()
    include_router(app)
    middleware(app)
    return app

app = start_application()


# ------------ Home Route ------------------
@app.get("/", tags=["Root"])
def home():
    return {"msg":"Hello from FastAPI Server 🚀"}



if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        reload=True,
        workers=1,
        host="0.0.0.0",
        port=51,
    )
    
