from typing import Optional

from apis.v1.route_login import get_current_user
from db.repository.merchant import create_new_merchant
from db.repository.merchant import delete_merchant
from db.repository.merchant import list_merchants
from db.repository.merchant import retreive_merchant
from db.repository.merchant import update_merchant
from db.session import get_db
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Form
from fastapi import Request
from fastapi import responses
from fastapi import status
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.templating import Jinja2Templates
from schemas.merchant import ShowMerchant, CreateMerchant
from sqlalchemy.orm import Session


templates = Jinja2Templates(directory="templates")
router = APIRouter()


@router.get("/")
def home(request: Request, alert: Optional[str] = None, db: Session = Depends(get_db)):
    blogs = list_merchants(db=db)
    return templates.TemplateResponse(
        "merchant/home.html", {"request": request, "blogs": blogs, "alert": alert}
    )


@router.get("/app/blog/{id}")
def blog_detail(request: Request, id: int, db: Session = Depends(get_db)):
    blog = retreive_merchant(id=id, db=db)
    return templates.TemplateResponse(
        "merchant/detail.html", {"request": request, "blog": blog}
    )


@router.get("/app/create-new-blog")
def create_blog(request: Request):
    return templates.TemplateResponse("merchant/create_blog.html", {"request": request})


@router.post("/app/create-new-blog")
def create_blog(
    request: Request,
    title: str = Form(...),
    content: str = Form(...),
    db: Session = Depends(get_db),
):
    token = request.cookies.get("access_token")
    _, token = get_authorization_scheme_param(token)
    try:
        author = get_current_user(token=token, db=db)
        blog = CreateMerchant(title=title, content=content)
        blog = create_new_merchant(blog=blog, db=db, author_id=author.id)
        return responses.RedirectResponse(
            "/?alert=Blog Submitted for Review", status_code=status.HTTP_302_FOUND
        )
    except Exception as e:
        errors = ["Please log in to create blog"]
        print("Exception raised", e)
        return templates.TemplateResponse(
            "merchant/create_blog.html",
            {"request": request, "errors": errors, "title": title, "content": content},
        )


@router.get("/delete/{id}")
def delete_a_blog(request: Request, id: int, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    _, token = get_authorization_scheme_param(token)
    try:
        author = get_current_user(token=token, db=db)
        msg = delete_merchant(id=id, author_id=author.id, db=db)
        alert = msg.get("error") or msg.get("msg")
        return responses.RedirectResponse(
            f"/?alert={alert}", status_code=status.HTTP_302_FOUND
        )
    except Exception as e:
        print(f"Exception raised while deleting {e}")
        blog = retreive_merchant(id=id, db=db)
        return templates.TemplateResponse(
            "merchant/detail.html",
            {"request": request, "alert": "Please Login Again", "blog": blog},
        )
