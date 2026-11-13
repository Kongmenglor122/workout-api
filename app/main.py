from fastapi import FastAPI

app = FastAPI(title="Workout API")


@app.get("/")
def root():
    return {"message": "Welcome to your Workout API"}