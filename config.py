import os

WS_URL = os.environ.get('WS_URL', '')

MYSQL_HOST = os.environ.get('MYSQL_HOST', '127.0.0.1:3306')
MYSQL_USER = os.environ.get('MYSQL_USER', 'user01')
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'a1234567')
MYSQL_DB = os.environ.get('MYSQL_DB', 'vocabilary_highlighter')
