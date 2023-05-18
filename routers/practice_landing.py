from fastapi import Request, APIRouter
from fastapi.templating import Jinja2Templates
from services.test_service import TestService
from utils.models import UserData

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/")
async def get_landing_page(request: Request):
    html_resp = templates.TemplateResponse("index.html", {"request": request})
    return html_resp



