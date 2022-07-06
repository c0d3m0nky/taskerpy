from typing import List, Dict

from fastapi import APIRouter
from psycopg2 import Error, sql

from .db import connect

# APIRouter creates path operations for user module
router = APIRouter(
    prefix="/tbay/threads",
    tags=["TBayMod: Threads"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_threads():
    conn = None
    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute('select * from public.threads')
        return {x[0]: x[1] for x in cur.fetchall()}
    except (Exception, Error) as error:
        return {"err": error}
    finally:
        if conn: conn.close()


@router.post("/")
async def check_threads(threads: List[str]):
    conn = None
    try:
        conn = connect()
        cur = conn.cursor()
        qry = sql.SQL('select * from public.threads where id in ({})').format(
            sql.SQL(',').join(map(sql.Literal, threads)))
        cur.execute(qry)
        return {x[0]: x[1] for x in cur.fetchall()}
    except (Exception, Error) as error:
        return {"err": error}
    finally:
        if conn: conn.close()


@router.put("/")
async def upsert_thread(key: str, data: dict):
    conn = None
    try:
        conn = connect()
        cur = conn.cursor()
        if data['ignore'] and (data['maybe'] or data['priority']):
            data['ignore'] = False
        cur.callproc('upsert_thread', (key, data))
        conn.commit()
        return {"success": True}
    except (Exception, Error) as error:
        return {"err": error}
    finally:
        if conn: conn.close()


@router.put("/bulk")
async def upsert_threads(threads: Dict[str, dict]):
    conn = None
    try:
        conn = connect()
        cur = conn.cursor()
        for k in threads:
            data = threads[k]
            if data['ignore'] and (data['maybe'] or data['priority']):
                data['ignore'] = False
            cur.callproc('upsert_thread', (k, data))
        conn.commit()
        return {"success": True}
    except (Exception, Error) as error:
        return {"err": error}
    finally:
        if conn: conn.close()
