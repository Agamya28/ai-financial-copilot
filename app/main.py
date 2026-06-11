from fastapi import FastAPI

from app.database.database import Base, engine
from app.database import models
from app.routers import transactions
from app.routers import users
from app.routers import auth

app = FastAPI()

app.include_router(auth.router)
app.include_router(transactions.router)
app.include_router(users.router)

Base.metadata.create_all(bind=engine)