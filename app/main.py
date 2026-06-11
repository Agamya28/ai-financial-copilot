from fastapi import FastAPI

from app.database.database import Base, engine
from app.database import models
from app.routers import transactions
from app.routers import users

app = FastAPI()

app.include_router(transactions.router)
app.include_router(users.router)

Base.metadata.create_all(bind=engine)