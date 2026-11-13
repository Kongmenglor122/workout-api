from fastapi import FastAPI
from app.routers import machines,workouts, workoutactivity

app = FastAPI(title="Workout API")


@app.get("/")
def root():
    return {"message": "Welcome to your Workout API"}

app.include_router(machines.router)
app.include_router(workouts.router)
app.include_router(workoutactivity.router)