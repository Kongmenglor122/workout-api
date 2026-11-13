from app import models, schemas
from app.database import get_db

from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import APIRouter, Depends, HTTPException, Response

router = APIRouter(
    prefix="/workouts/{id}/activities",
    tags=["Workout Activities"],
)

@router.post("", status_code=201, response_model=schemas.WorkoutActivityResponse)
def create_workout_activity(workout_id: int, body: schemas.WorkoutActivityCreate, db: Session = Depends(get_db), ):

    workout = db.get(models.Workout, workout_id)
    machine = db.get(models.Machine, body.machine_id)

    if workout is None:
        raise HTTPException(status_code=404, detail="Workout not found")

    if workout.ended_at is not None:
        raise HTTPException(
            status_code=409,
            detail="Cannot add activity to a finished workout"
        )

    if machine is None:
        raise HTTPException(status_code=404, detail="machine not found")

    workout_activity = models.WorkoutActivity(started_at = body.started_at, workout_id = workout.id, machine_id = body.machine_id)
    db.add(workout_activity)
    db.commit()
    db.refresh(workout_activity)

    return workout_activity
