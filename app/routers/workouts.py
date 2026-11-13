from app import models, schemas
from app.database import get_db

from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import APIRouter, Depends, HTTPException, Response


router = APIRouter(
    prefix="/workouts",
    tags=["Workouts"],
)

@router.post(
    "",
    status_code=201,
    response_model=schemas.WorkoutResponse,
)
def create_workout(
    workout: schemas.WorkoutCreate,
    db: Session = Depends(get_db),
):
    new_workout = models.Workout(
        started_at=workout.started_at,
        notes=workout.notes,
    )

    db.add(new_workout)
    db.commit()
    db.refresh(new_workout)

    return new_workout

@router.get("", response_model=list[schemas.WorkoutResponse])
def get_all_workouts(db: Session = Depends(get_db)):
    statement = select(models.Workout).order_by(models.Workout.id)
    all_workouts = db.scalars(statement).all()

    return all_workouts