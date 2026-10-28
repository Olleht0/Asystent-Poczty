from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.emails import router as emails_router
from app.database.connection import Base, engine
from app.models import database_models  # rejestracja tabel


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Email Assistant API",
    description="Backend asystenta poczty elektronicznej",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(emails_router)


@app.get("/")
def root():
    return {"message": "Email Assistant API działa!"}