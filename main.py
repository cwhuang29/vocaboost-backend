import time
import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from routers import auth, user, word
from utils.logger import parseRequestLogFormat

logger = logging.getLogger(__name__)

origins = ["http://localhost", "http://localhost:8080"]

app = FastAPI()

app.include_router(prefix="/v1", router=auth.router)
app.include_router(prefix="/v1", router=user.router)
app.include_router(prefix="/v1", router=word.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    max_age=1800,
    allow_methods=['GET', 'POST', 'PUT', 'OPTIONS'],
    allow_headers=["Accept", "Authorization", "Content-Type", "Content-Length", "Accept-Encoding", "X-CSRF-Token", "X-VH-Source"],
    expose_headers=['X-VH-Source']
)


@app.middleware("http")
async def add_process_time_header(req: Request, call_next):
    start_time = time.time()
    response = await call_next(req)
    process_time = time.time() - start_time
    logger.warning(parseRequestLogFormat(req, process_time))
    response.headers["X-VH-Source"] = 'backend'
    return response


@app.get("/")
def read_root():
    return {"Hello": "This is the backend server of Vocabulary Highlighter"}
