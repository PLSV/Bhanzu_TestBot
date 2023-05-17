import uvicorn
from fastapi import FastAPI
import logging
from fastapi.responses import JSONResponse

app = FastAPI()

logger = logging.getLogger("gunicorn.error")

@app.get("/")
def read_root():
    return JSONResponse(
        content={"Hello": "World"}
    )

if __name__ == "__main__":
    logger.info("Starting fast api app for CLM service")
    uvicorn.run(app="main:app", host="0.0.0.0", port=80, reload=True)