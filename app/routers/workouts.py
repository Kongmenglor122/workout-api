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

@router.get("/{id}", response_model=schemas.WorkoutResponse)
def get_workout_by_id(id: int, db: Session = Depends(get_db)):
    workout = db.get(models.Workout, id)

    if workout is None:
        raise HTTPException(
            status_code=404,
            detail=f'Cannot find workout by {id}'
        )
    return workout

@router.delete("/{id}", status_code=204)
def delete_workout_by_id(id: int, db: Session = Depends(get_db)):
    workout = db.get(models.Workout, id)
    if workout is None:
        raise HTTPException(
            status_code=404,
            detail=f'Item is not found by this {id}'
        )
    db.delete(workout)
    db.commit()

    return Response(status_code=204)

@router.patch("/{id}/finish", response_model=schemas.WorkoutResponse)
def patch_by_id(id: int, updates: schemas.WorkoutFinish, db: Session = Depends(get_db)):
    
    workout = db.get(models.Workout, id)
    if workout is None:
        raise HTTPException(
            status_code=404,
            detail=f'Cannot by update by this {id}'
        )
    if workout.ended_at is not None:
        raise HTTPException(
            status_code=409,
            detail= "Workout session is done already."
        )
    if updates.ended_at < workout.started_at:
        raise HTTPException(
            status_code=422,
            detail="Cannot update finish time before starting time."
        )
    workout.ended_at = updates.ended_at
    if (updates.notes is not None):
        workout.notes = updates.notes

    db.commit()
    db.refresh(workout)

    return workout
