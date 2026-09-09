from fastapi import FastAPI
from database import Base, engine
from routes.categories import router as cat_router
from routes.accounts import router as acc_router
from routes.transactions import router as trans_router
from routes.reports import router as rep_router
from seed import seed

app = FastAPI()

Base.metadata.create_all(bind=engine)

seed()

app.include_router(cat_router)
app.include_router(acc_router)
app.include_router(trans_router)
app.include_router(rep_router)
