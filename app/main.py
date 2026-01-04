from contextlib import asynccontextmanager

from fastapi import FastAPI

from .core.cors import setup_cors
from .core.logging import setup_logging
from .db.session import create_db_and_tables
from .routers import speakers

setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI()

setup_cors(app)

app.include_router(speakers.router)
