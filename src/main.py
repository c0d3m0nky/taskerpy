import uvicorn
from fastapi import FastAPI
from api import router
from fastapi.middleware.cors import CORSMiddleware

from tbay import db

db.test_db()

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
async def root():
    return {"message": "Howdy World"}


if __name__ == '__main__':
    uvicorn.run("main:app", host='127.0.0.1', port=8000, log_level="info", reload=True)
    print("running")
    print("http://localhost:8000/docs")
