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

# def close(self):
#     if self.conn:
#         # if cur:
#         #     cur.close()
#         self.conn.close()


