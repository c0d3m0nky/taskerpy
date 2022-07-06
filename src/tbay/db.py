from os import environ as env
import psycopg2
from psycopg2 import extensions, extras

psycopg2.extensions.register_adapter(dict, psycopg2.extras.Json)


def connect():
    return psycopg2.connect(user=env['PGUSER'],
                            password=env['PGPWD'],
                            host=env['PGHOST'],
                            port=env['PGPORT'],
                            database=env['PGTBDB'] if 'PGTBDB' in env else 'tbay_mod')


def dispose(conn, cur):
    if conn:
        if cur:
            cur.close()
        conn.close()


def test_db():
    conn = None
    cur = None
    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute('select count(1) from public.threads')
    except (Exception, psycopg2.Error) as error:
        raise
    finally:
        dispose(conn, cur)

