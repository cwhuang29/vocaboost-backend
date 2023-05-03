import os

MYSQL_HOST = os.environ.get('MYSQL_HOST', '127.0.0.1:3306')
MYSQL_USER = os.environ.get('MYSQL_USER', 'vocaboost')
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'a1234567')
MYSQL_DB = os.environ.get('MYSQL_DB', 'vocaboost')

JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', '')
JWT_ALGO = os.environ.get('JWT_ALGO', 'HS256')
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get('JWT_ACCESS_TOKEN_EXPIRE_MINUTES', '21600')

GOOGLE_LOGIN_IOS_CLIENT_ID = os.environ.get('GOOGLE_LOGIN_IOS_CLIENT_ID', '')
AZURE_LOGIN_CLIENT_ID = os.environ.get('AZURE_LOGIN_CLIENT_ID', '')
