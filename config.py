import os

WS_URL = os.environ.get('WS_URL', '')

MYSQL_HOST = os.environ.get('MYSQL_HOST', '127.0.0.1:3306')
MYSQL_USER = os.environ.get('MYSQL_USER', 'user01')
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'a1234567')
MYSQL_DB = os.environ.get('MYSQL_DB', 'vocabilary_highlighter')

JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', '9e283bd0313d49ca307f2fdc4b9d4ad8ae8cc63a0d14406791b2c4ce54bf860d')
JWT_ALGO = os.environ.get('JWT_ALGO', 'HS256')
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get('JWT_ACCESS_TOKEN_EXPIRE_MINUTES', '60')
