from fastapi import APIRouter
from psycopg2 import Error

import db

router = APIRouter(
    prefix="/tbay/settings",
    tags=["TBayMod: Settings"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{id}")
async def get_settings(id: str):
    conn = None
    cur = None
    try:
        conn = db.connect()
        cur = conn.cursor()
        cur.execute("select s.data from public.settings s where id = %s;", (id,))
        res = cur.fetchone()

        if res:
            return res[0]
        else:
            return {}
    except (Exception, Error) as error:
        return {"err": error}
    finally:
        db.dispose(conn, cur)


@router.put("/{id}")
async def upsert_setting(id: str, data: dict):
    conn = None
    cur = None
    try:
        conn = db.connect()
        cur = conn.cursor()
        cur.callproc('upsert_setting', (id, data))
        conn.commit()
        return {"success": True}
    except (Exception, Error) as error:
        return {"err": error}
    finally:
        db.dispose(conn, cur)
