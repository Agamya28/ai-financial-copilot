from fastapi import FastAPI

from app.database.database import Base, engine
from app.database import models
from app.routers import transactions
from app.routers import users
from app.routers import auth
from app.routers import analytics
from app.routers import ai
from app.routers import csv_upload

app = FastAPI()

app.include_router(auth.router)
app.include_router(transactions.router)
app.include_router(users.router)
app.include_router(analytics.router)
app.include_router(ai.router)
app.include_router(csv_upload.router)

Base.metadata.create_all(bind=engine)