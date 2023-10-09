import time

from apis.neo import NeoAPI
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from pydantic import BaseModel

from fastapi.middleware.cors import CORSMiddleware

neo = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    neo = NeoAPI()
    yield
    # Clean up the ML models and release the resources
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

