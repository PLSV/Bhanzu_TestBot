from fastapi import Request, APIRouter


router = APIRouter(prefix="/practice")


@router.get("/receive/user")
async def get_question(request: Request):
    return "tettee"


@router.post("/capture/response")
async def capture_response():
    pass
