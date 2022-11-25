import uvicorn
from os import environ as env
from fastapi import FastAPI, Request
from api import router
from fastapi.middleware.cors import CORSMiddleware
import psycopg2


def test_db():
    db = None
    try:
        db = psycopg2.connect(user=env['PGUSER'],
                              password=env['PGPWD'],
                              host=env['PGHOST'],
                              port=env['PGPORT'],
                              database='postgres')
        cur = db.cursor()
        cur.execute('select 1')
    except (Exception, psycopg2.Error) as error:
        raise
    finally:
        if db: db.close()


test_db()

app = FastAPI()

app.include_router(router)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root(request: Request):
    return {"docs": f'{request.url.scheme}://{request.url.netloc}/docs'}


if __name__ == '__main__':
    uvicorn.run("main:app", host='127.0.0.1', port=8000, log_level="info", reload=True)
    print("running")
    print("http://localhost:8000/docs")
