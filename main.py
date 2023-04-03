import time
import logging


from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from utils.logger import parseRequestLogFormat

from routers import auth, user, word

logger = logging.getLogger(__name__)

app = FastAPI()

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(word.router)

origins = ["http://localhost", "http://localhost:8080"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    max_age=1800,
    allow_methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
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
    return {"Hello": "This is the backend server of Vocabilary Highlighter"}
