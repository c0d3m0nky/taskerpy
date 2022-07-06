from typing import List, Dict

from fastapi import APIRouter
from psycopg2 import Error, sql

from .db import Db

# APIRouter creates path operations for user module
router = APIRouter(
    prefix="/tbay/threads",
    tags=["TBayMod: Threads"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_threads():
    db = None
    try:
        db = Db()
        cur = db.conn.cursor()
        cur.execute('select * from public.threads')
        return {x[0]: x[1] for x in cur.fetchall()}
    except (Exception, Error) as error:
        return {"err": error}
    finally:
        db.close()


@router.post("/")
async def check_threads(threads: List[str]):
    db = None
    try:
        db = Db()
        cur = db.conn.cursor()
        qry = sql.SQL('select * from public.threads where id in ({})').format(
            sql.SQL(',').join(map(sql.Literal, threads)))
        cur.execute(qry)
        return {x[0]: x[1] for x in cur.fetchall()}
    except (Exception, Error) as error:
        return {"err": error}
    finally:
        db.close()


@router.put("/")
async def upsert_thread(key: str, data: dict):
    db = None
    try:
        db = Db()
        cur = db.conn.cursor()
        if data['ignore'] and (data['maybe'] or data['priority']):
            data['ignore'] = False
        cur.callproc('upsert_thread', (key, data))
        db.conn.commit()
        return {"success": True}
    except (Exception, Error) as error:
        return {"err": error}
    finally:
        db.close()


@router.put("/bulk")
async def upsert_threads(threads: Dict[str, dict]):
    db = None
    try:
        db = Db()
        cur = db.conn.cursor()
        for k in threads:
            data = threads[k]
            if data['ignore'] and (data['maybe'] or data['priority']):
                data['ignore'] = False
            cur.callproc('upsert_thread', (k, data))
        db.conn.commit()
        return {"success": True}
    except (Exception, Error) as error:
        return {"err": error}
    finally:
        db.close()
