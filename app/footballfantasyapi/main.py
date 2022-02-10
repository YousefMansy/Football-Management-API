import time
from fastapi import FastAPI, APIRouter, Request

from app.footballfantasyapi.core.config import settings
from app.footballfantasyapi.api.api_v1.api import api_router

root_router = APIRouter()
app = FastAPI(title="Fantasy Football API")


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(root_router, tags=['Root'])

if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
