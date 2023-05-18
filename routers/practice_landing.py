from fastapi import Request, APIRouter
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/")
async def get_landing_page(request: Request):
    html_resp = templates.TemplateResponse("index.html", {"request": request})
    return html_resp



