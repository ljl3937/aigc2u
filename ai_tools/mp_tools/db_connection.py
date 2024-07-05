import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def get_mysql_connection():
    return mysql.connector.connect(
        host=os.environ['MYSQL_HOST'],
        user=os.environ['MYSQL_USER'],
        password=os.environ['MYSQL_PASSWORD'],
        database=os.environ['MYSQL_DB']
    )

def close_mysql_connection(conn):
    if conn:
        conn.close()
