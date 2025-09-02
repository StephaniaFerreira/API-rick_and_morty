from fastapi import FastAPI
from controllers import controller
from database import Base, engine

app = FastAPI()

app.include_router(controller.router)

Base.metadata.create_all(bind=engine)