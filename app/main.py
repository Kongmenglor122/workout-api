from fastapi import FastAPI
from app.routers import machines

app = FastAPI(title="Workout API")


@app.get("/")
def root():
    return {"message": "Welcome to your Workout API"}

app.include_router(machines.router)