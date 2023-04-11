import time
import logging

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse

from routers import auth, user, word
from utils.constant import FAVICON_PATH
from utils.logger import parseRequestLogFormat

logger = logging.getLogger(__name__)

app = FastAPI(docs_url=None, redoc_url=None)

app.include_router(prefix='/v1', router=auth.router)
app.include_router(prefix='/v1', router=user.router)
app.include_router(prefix='/v1', router=word.router)
app.mount("/privacy-policy", StaticFiles(directory="privacy-policy", html=True), name="privacy-policy")


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    max_age=1800,
    allow_methods=['GET', 'POST', 'PUT', 'OPTIONS'],
    allow_headers=['Accept', 'Authorization', 'Content-Type', 'Content-Length', 'Accept-Encoding', 'X-CSRF-Token', 'X-VH-Source'],
)


@app.middleware('http')
async def add_process_time_header(req: Request, call_next):
    start_time = time.time()
    response = await call_next(req)
    process_time = time.time() - start_time
    logger.warning(parseRequestLogFormat(req, process_time))
    response.headers['X-VH-Source'] = 'backend'
    return response


@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse(FAVICON_PATH)


@app.get('/')
def read_root():
    return {'Hello': 'This is the backend server of VocaBoost'}
