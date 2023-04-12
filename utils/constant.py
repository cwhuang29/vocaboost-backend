FAVICON_PATH = 'assets/favicon.ico'

OAUTH_GOOGLE_ISS = ['accounts.google.com', 'https://accounts.google.com']

CORS = {
    'HOSTS': ['*.vocabularyboost.com'],
    'METHODS': ['GET', 'POST', 'PUT', 'OPTIONS'],
    'HEADERS': ['Accept', 'Authorization', 'Content-Type', 'Content-Length', 'Accept-Encoding', 'X-CSRF-Token', 'X-VH-Source'],
}

HEADER_SOURCE = {
    'NAME': 'X-VH-Source',
    'VALUE': 'backend',
}
