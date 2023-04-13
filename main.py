import time
import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from routers import auth, user, word
from utils.constant import CORS, FAVICON_PATH, HEADER_SOURCE
from utils.logger import showRequestStat

logger = logging.getLogger(__name__)

app = FastAPI(docs_url=None, redoc_url=None)

app.include_router(prefix='/v1', router=auth.router)
app.include_router(prefix='/v1', router=user.router)
app.include_router(prefix='/v1', router=word.router)
app.mount('/support', StaticFiles(directory='static/support', html=True), name='support')
app.mount('/privacy-policy', StaticFiles(directory='static/privacy-policy', html=True), name='privacy-policy')


app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS['HOSTS'],
    allow_credentials=True,
    max_age=1800,
    allow_methods=CORS['METHODS'],
    allow_headers=CORS['HEADERS'],
)


@app.middleware('http')
async def add_process_time_header(req: Request, call_next):
    start_time = time.time()
    resp = await call_next(req)
    resp.headers[HEADER_SOURCE['NAME']] = HEADER_SOURCE['VALUE']
    showRequestStat(req, resp, time.time() - start_time)
    return resp


@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse(FAVICON_PATH)


@app.get('/')
def read_root():
    return {'Hello': 'This is the backend server of VocaBoost'}
