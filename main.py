from fastapi import FastAPI
import models
from database import engine
from routes import router

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Globant API")

app.include_router(router)

@app.get("/")
def root():
    return {"message": "API is running"}