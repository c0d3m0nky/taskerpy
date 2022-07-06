from os import environ as env
import psycopg2
from psycopg2 import extensions, extras

psycopg2.extensions.register_adapter(dict, psycopg2.extras.Json)


class Db:

    def __init__(self):
        self.conn = psycopg2.connect(user=env['PGUSER'],
                                password=env['PGPWD'],
                                host=env['PGHOST'],
                                port=env['PGPORT'],
                                database=env['PGTBDB'] if 'PGTBDB' in env else 'tbay_mod')

    def close(self):
        if self.conn:
            # if cur:
            #     cur.close()
            self.conn.close()

    # def test_db(self):
    #     conn = None
    #     cur = None
    #     try:
    #         conn = self.connect()
    #         cur = conn.cursor()
    #         cur.execute('select count(1) from public.threads')
    #     except (Exception, psycopg2.Error) as error:
    #         raise
    #     finally:
    #         self.dispose(conn, cur)
