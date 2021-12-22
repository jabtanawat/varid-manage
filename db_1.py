import pymysql

HOST = "127.0.0.1"
USER = "admin"
PASS = "j@b25J1Kkim27"
DATABASE = "dbvarid14"

def mysql_connect():
    global conn    
    conn = pymysql.connect(host=HOST, user=USER, passwd=PASS, db=DATABASE)

def run_query_fetchall(sql):
    mysql_connect()
    with conn.cursor() as cur:
        cur.execute(sql)
        row = cur.fetchall()
    conn.close()
    return row

def run_query_fetchone(sql):
    mysql_connect()
    with conn.cursor() as cur:
        cur.execute(sql)
        info = cur.fetchone()
    conn.close()
    return info

def run_query_commit(sql, string):
    mysql_connect()
    with conn.cursor() as cur:
        cur.execute(sql, (string))
        conn.commit()
    conn.close()

def run_commit(sql):
    mysql_connect()
    with conn.cursor() as cur:
        cur.execute(sql)
        conn.commit()
    conn.close()