FAVICON_PATH = 'assets/favicon.ico'

OAUTH_GOOGLE_ISS = ['accounts.google.com', 'https://accounts.google.com']

OAUTH_AZURE_ISS = 'https://login.microsoftonline.com'

OAUTH_AZURE_JWKS_URI = 'https://login.microsoftonline.com/common/discovery/v2.0/keys'

OAUTH_AZURE_VER = '2.0'

CORS = {
    'HOSTS': ['*'],  # Extension's content script initiates requests on every webpage
    'METHODS': ['GET', 'POST', 'PUT', 'OPTIONS'],
    'HEADERS': ['Accept', 'Authorization', 'Content-Type', 'Content-Length', 'Accept-Encoding', 'X-CSRF-Token', 'X-VH-Source'],
}

HEADER_SOURCE = {
    'NAME': 'X-VH-Source',
    'VALUE': 'backend',
}
