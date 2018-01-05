'''a db service provider '''
from config import DB_USER, DB_PWD, DB_NAME, DB_HOST

import MySQLdb

def getconn():
    conn = MySQLdb.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PWD,
    db=DB_NAME
    )
    return conn