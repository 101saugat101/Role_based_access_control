from fastapi import FastAPI
from app.api.endpoints import documents
from app.database.database import engine
from app.model import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(documents.router, prefix="/api/v1", tags=["Documents"])
