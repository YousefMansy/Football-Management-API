import time
from functools import lru_cache
from sqlalchemy.orm import Session
from fastapi import FastAPI, APIRouter, Depends, HTTPException, Request

from footballfantasyapi import crud
from footballfantasyapi.api import deps
from footballfantasyapi.core.config import settings
from footballfantasyapi.api.api_v1.api import api_router

root_router = APIRouter()
app = FastAPI(title="Fantasy Football API")


# @lru_cache()
# def get_settings():
#     return settings()


@root_router.get("/", status_code=200)
def root(
        request: Request,
        db: Session = Depends(deps.get_db)
) -> dict:
    """
    Root GET
    """
    return crud.team.get_multi(db=db)


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
