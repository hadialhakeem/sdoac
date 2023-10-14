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
    "http://localhost:5173"
]

app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/path")
def path(src_id: int, dest_id: int):
    shortest_path = neo.shortest_path(src_id, dest_id)

    if not shortest_path:
        return {
            "path": None
        }

    nodes, path_length, weight = shortest_path

    return {
        "path": {
            "nodes": nodes,
            "length": path_length,
            "degrees": path_length//2,
        }
    }


@app.get("/search")
def search_characters(q: str):
    if q == "":
        return {
            "data": []
        }

    characters = neo.search_character_by_name(q)
    return {
        "data": characters
    }


