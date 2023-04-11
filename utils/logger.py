from datetime import datetime
import time

from fastapi import Request


def parseRequestLogFormat(req: Request, process_time: time):
    method = req.method
    url = req.url
    clientHost = req.client.host
    clientPort = req.client.port
    path_params = req.path_params
    query_params = req.query_params
    headers = req.headers
    # cookies = req.cookies
    return f'Time: {datetime.utcnow()}. Method: {method}. Client IP: {clientHost}. Client Port: {clientPort}. URL: {url}. Path params: {path_params}. Query params: {query_params}, Headers: {headers}. Time spent: {process_time}'
