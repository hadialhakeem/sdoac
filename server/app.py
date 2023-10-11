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


@app.get("/path")
def path(src_id: int, dest_id: int):
    result = neo.shortest_path(src_id, dest_id)
    return {
        "path": result
    }


class SearchRequestData(BaseModel):
    character_name: str


@app.get("/search")
def path(q: str):
    if q == "":
        return []

    characters = neo.search_character_by_name(q)
    return characters


