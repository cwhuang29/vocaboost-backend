from config import MYSQL_DB, MYSQL_HOST, MYSQL_PASSWORD, MYSQL_USER


def getDBURL():
    url = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}'
    return url
