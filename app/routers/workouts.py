from app import models, schemas
from app.database import get_db

from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import APIRouter, Depends, HTTPException, Response
from app.dependencies import get_current_user

# workouts.py
router = APIRouter(
    prefix="/workouts",
    tags=["Workouts"],
    dependencies=[Depends(get_current_user)],
)

@router.post(
    "",
    status_code=201,
    response_model=schemas.WorkoutResponse,
)
def create_workout(
    workout: schemas.WorkoutCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    new_workout = models.Workout(
        user_id=current_user.id,
        started_at=workout.started_at,
        notes=workout.notes,
    )

    db.add(new_workout)
    db.commit()
    db.refresh(new_workout)

    return new_workout

@router.get("", response_model=list[schemas.WorkoutResponse])
def get_all_workouts(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    statement = (
        select(models.Workout)
        .where(models.Workout.user_id == current_user.id)
        .order_by(models.Workout.id)
    )

    return db.scalars(statement).all()

@router.get("/{id}", response_model=schemas.WorkoutResponse)
def get_workout_by_id(id: int, db: Session = Depends(get_db),current_user: models.User = Depends(get_current_user),):
    workout = db.get(models.Workout, id,models.Workout.user_id == current_user.id,)

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
def patch_by_id(
    id: int,
    updates: schemas.WorkoutFinish,
    db: Session = Depends(get_db),
):
    workout = db.get(models.Workout, id)

    if workout is None:
        raise HTTPException(status_code=404, detail="Workout not found")

    if workout.ended_at is not None:
        raise HTTPException(
            status_code=409,
            detail="Workout has already finished.",
        )

    statement = select(models.WorkoutActivity).where(
        models.WorkoutActivity.workout_id == id,
        models.WorkoutActivity.ended_at.is_(None),
    )
    active_activity = db.scalars(statement).first()

    if active_activity is not None:
        raise HTTPException(
            status_code=409,
            detail="Finish your current activity before finishing the workout.",
        )

    if updates.ended_at <= workout.started_at:
        raise HTTPException(
            status_code=422,
            detail="End time must be after start time.",
        )

    workout.ended_at = updates.ended_at

    if updates.notes is not None:
        workout.notes = updates.notes

    db.commit()
    db.refresh(workout)

    return workout
