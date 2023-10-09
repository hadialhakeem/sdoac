import time

from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from extensions import neo

from fastapi.middleware.cors import CORSMiddleware


load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    neo.connect()
    yield
    neo.close()


origins = [
    "http://localhost:8000"
]

app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


class PathRequestData(BaseModel):
    src_id: int
    dest_id: int


@app.post("/path")
def path(req: PathRequestData):
    return req


class SearchRequestData(BaseModel):
    character_name: str


@app.post("/search")
def path(req: SearchRequestData):
    neo.search_character_by_name(req.character_name)
    return req

