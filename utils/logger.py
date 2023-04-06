import time

from fastapi import Request


def parseRequestLogFormat(req: Request, process_time: time):
    method = req.method
    domain = req.base_url
    url = req.url
    path_params = req.path_params
    query_params = req.query_params
    headers = req.headers
    # cookies = req.cookies
    return f'Method: {method}.Domain: {domain}. URL: {url}. Path params: {path_params}. Query params: {query_params}, Headers: {headers}. Time spent: {process_time}'
