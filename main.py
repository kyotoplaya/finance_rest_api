from fastapi import FastAPI
from database import Base, engine
from routes.categories import router
from seed import seed

app = FastAPI()

Base.metadata.create_all(bind=engine)

seed()

app.include_router(router)
