import psycopg2
from typing import List, Tuple, Union
from consts import database_consts

cursor = None

def get_cursor():
    global cursor
    if cursor is None:
        conn = psycopg2.connect(user="postgres",
                                password="nofar0544",
                                host="127.0.0.1",
                                port="5432",
                                database="nofarlevy")
        cursor = conn.cursor()
        conn.commit()
