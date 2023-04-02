import time

from fastapi import Request


def parseRequestLogFormat(req: Request, process_time: time):
    method = req.method
    url = req.base_url
    path_params = req.path_params
    query_params = req.query_params
    # headers = req.headers
    # cookies = req.cookies
    return f"Method: {method}. URL: {url}. Path: {path_params}. Query: {query_params}. Time spent: {process_time}"
