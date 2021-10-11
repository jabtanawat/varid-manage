import pymysql
import logging
import sshtunnel
from sshtunnel import SSHTunnelForwarder

ssh_host = '27.254.174.33'
ssh_username = 'ubuntu'
ssh_password = 'j@b25J1Kkim27'
database_username = 'admin'
database_password = 'j@b25J1Kkim27'
database_name = 'dbvarid14'
localhost = '127.0.0.1'

def open_ssh_tunnel(verbose=False):
    
    if verbose:
        sshtunnel.DEFAULT_LOGLEVEL = logging.DEBUG
    
    global tunnel

    tunnel = SSHTunnelForwarder(
        (ssh_host, 22),
        ssh_username = ssh_username,
        ssh_password = ssh_password,
        remote_bind_address = ('127.0.0.1', 3306)
    )
    
    tunnel.start()

def mysql_connect():

    global connection
    
    connection = pymysql.connect(
        host='127.0.0.1',
        user=database_username,
        passwd=database_password,
        db=database_name,
        port=tunnel.local_bind_port
    )

def run_query_fetchall(sql):

    open_ssh_tunnel()
    mysql_connect()

    with connection.cursor() as cur:
        cur.execute(sql)
        row = cur.fetchall()

    mysql_disconnect()
    close_ssh_tunnel()

    return row

def run_query_fetchone(sql):
    open_ssh_tunnel()
    mysql_connect()
    with connection.cursor() as cur:
        cur.execute(sql)
        info = cur.fetchone()
    mysql_disconnect()
    close_ssh_tunnel()
    return info

def run_query_commit(sql, executes):
    open_ssh_tunnel()
    mysql_connect()
    with connection.cursor() as cur:
        cur.execute(sql, executes)
        connection.commit()
    mysql_disconnect()
    close_ssh_tunnel()
    return print("ok")

def run_commit(sql):
    open_ssh_tunnel()
    mysql_connect()
    with connection.cursor() as cur:
        cur.execute(sql)
        connection.commit()
    mysql_disconnect()
    close_ssh_tunnel()
    return print("ok")

def mysql_disconnect():    
    connection.close()

def close_ssh_tunnel():
    tunnel.close