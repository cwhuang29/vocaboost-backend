import time
import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from routers import auth, user, word
from utils.constant import CORS, FAVICON_PATH, HEADER_SOURCE, HEADER_SOURCE_VALUE
from utils.logger import showRequestStat

logger = logging.getLogger(__name__)

app = FastAPI(docs_url=None, redoc_url=None)

app.include_router(prefix='/v1', router=auth.router)
app.include_router(prefix='/v1', router=user.router)
app.include_router(prefix='/v1', router=word.router)

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
    resp.headers[HEADER_SOURCE] = HEADER_SOURCE_VALUE
    showRequestStat(req, resp, time.time() - start_time)
    return resp


@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse(FAVICON_PATH)


@app.get('/.well-known/microsoft-identity-association.json')
def microsoftOAuthVerify():
    content = {"associatedApplications": [{"applicationId": "2d22f996-9c5c-476a-9f40-50a95f34f600"}]}
    return JSONResponse(content=content)


# This mounting should be placed in the last
app.mount('/', StaticFiles(directory='static', html=True), name='home')
