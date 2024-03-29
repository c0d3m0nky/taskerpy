from typing import List, Dict, Union

from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from psycopg2 import Error, sql

from .db import connect

# APIRouter creates path operations for user module
router = APIRouter(
    prefix="/tbay/threads",
    tags=["TBayMod: Threads"],
    responses={404: {"description": "Not found"}},
)


def err_response(error: Union[Dict, str]) -> JSONResponse:
    if isinstance(error, str):
        error = {'err': error}
    json_compatible_item_data = jsonable_encoder(error)
    return JSONResponse(content=json_compatible_item_data, status_code=500)


@router.get("/")
async def get_threads():
    conn = None
    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute('select * from public.threads')
        return {x[0]: x[1] for x in cur.fetchall()}
    except (Exception, Error) as error:
        return err_response(error)
    finally:
        if conn: conn.close()


@router.post("/")
async def check_threads(threads: List[int]):
    conn = None
    try:
        conn = connect()
        cur = conn.cursor()
        qry = cur.mogrify('select * from public.threads where id2 in ({0})'.format(','.join(str(i) for i in threads)))
        cur.execute(qry)
        res = cur.fetchall()
        return {x[4]: x[1] for x in res}
    except (Exception, Error) as error:
        return err_response(error)
    finally:
        if conn: conn.close()


@router.put("/")
async def upsert_thread(key: str, id2: int, data: dict):
    conn = None
    try:
        conn = connect()
        cur = conn.cursor()
        if ('maybe' in data and data['maybe']) or ('priority' in data and data['priority']):
            data['ignore'] = False
        cur.callproc('upsert_thread', (key, id2, data))
        conn.commit()
        return {"success": True}
    except (Exception, Error) as error:
        return err_response(error)
    finally:
        if conn: conn.close()


@router.put("/bulk")
async def upsert_threads(threads: Dict[str, dict]):
    conn = None
    try:
        conn = connect()
        cur = conn.cursor()
        for k in threads:
            id2 = int(threads[k]['id2'])
            data = threads[k]
            if ('maybe' in data and data['maybe']) or ('priority' in data and data['priority']):
                data['ignore'] = False
            cur.callproc('upsert_thread', (k, id2, data))
        conn.commit()
        return {"success": True}
    except (Exception, Error) as error:
        return err_response(error)
    finally:
        if conn: conn.close()
