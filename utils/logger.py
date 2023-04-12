from datetime import datetime
import logging
import time

from fastapi import Request, Response

logger = logging.getLogger(__name__)


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

    s = f'Time: {datetime.utcnow()}. Status Code: {statusCode}. Method: {method}. URL: {url}. Client IP: {clientHost}. Client Port: {clientPort}. Path params: {path_params}. Query params: {query_params}, Headers: {headers}. Time spent: {process_time}'
    logger.warning(s)
