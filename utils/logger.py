from datetime import datetime
import logging
import time

from fastapi import Request, Response
from fastapi.exceptions import RequestValidationError

logger = logging.getLogger(__name__)


# When a request contains invalid data, FastAPI internally raises a RequestValidationError
def showInvalidRequest(req: Request, exc: RequestValidationError):
    url = req.url
    method = req.method
    path_params = req.path_params
    query_params = req.query_params
    error = str(exc)
    s = f'[INVALID PAYLOAD] Time: {datetime.utcnow()}. Method: {method}. URL: {url}. Path params: {path_params}. Query params: {query_params}. Error: {error}'
    logger.error(s)


def showRequestStat(req: Request, resp: Response, process_time: time):
    statusCode = resp.status_code
    method = req.method
    url = req.url
    clientHost = req.client.host
    clientPort = req.client.port
    path_params = req.path_params
    query_params = req.query_params
    headers = req.headers
    # cookies = req.cookies

    s = f'Time: {datetime.utcnow()}. Status Code: {statusCode}. Method: {method}. URL: {url}. Client IP: {clientHost}. Client Port: {clientPort}. Path params: {path_params}. Query params: {query_params}. Headers: {headers}. Time spent: {process_time}'
    logger.warning(s)
