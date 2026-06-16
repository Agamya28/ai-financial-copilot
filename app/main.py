from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.database import Base, engine
from app.database import models
from app.routers import transactions
from app.routers import users
from app.routers import auth
from app.routers import analytics
from app.routers import ai
from app.routers import csv_upload
from app.routers import budget

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(transactions.router)
app.include_router(users.router)
app.include_router(analytics.router)
app.include_router(ai.router)
app.include_router(csv_upload.router)
app.include_router(budget.router)

Base.metadata.create_all(bind=engine)