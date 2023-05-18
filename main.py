import json

import uvicorn
from fastapi import FastAPI
import logging
from fastapi.responses import JSONResponse
from services import prompt_service
from fastapi import Request
from exceptions.application_exception import ApplicationException
from helpers.response_helper import ErrorResponse
from routers.routers_source import router

app = FastAPI()
app.include_router(router)
logger = logging.getLogger("gunicorn.error")


@app.post("/introduction")
async def introduce_yourself(
    request: Request,
):
    try:
        body = await request.body()
        body_str = body.decode()
        data_dict = json.loads(body_str)
        return JSONResponse(main_service.introfunction(data_dict))
    except ApplicationException as ae:
        error_response = ErrorResponse(ae.error, "application-exception")
        return JSONResponse(content=error_response.dict(), status_code=ae.status_code)


if __name__ == "__main__":
    logger.info("Starting fast api app for CLM service")
    uvicorn.run(app="main:app", host="0.0.0.0", port=80, reload=True)
