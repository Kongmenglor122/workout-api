from app import models, schemas
from app.database import get_db

from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import APIRouter, Depends, HTTPException
from app.dependencies import get_current_user

# workoutactivity.py
router = APIRouter(
    prefix="/workouts/{workout_id}/activities",
    tags=["Workout Activities"],
    dependencies=[Depends(get_current_user)],
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


    statement = select(models.WorkoutActivity).where(
        models.WorkoutActivity.workout_id == workout_id,
        models.WorkoutActivity.ended_at.is_(None),
    )

    active_activity = db.scalars(statement).first()

    if active_activity is None:
        workout_activity = models.WorkoutActivity(started_at = body.started_at, workout_id = workout.id, machine_id = body.machine_id)
        db.add(workout_activity)
        db.commit()
        db.refresh(workout_activity)

        return workout_activity

    raise HTTPException(
        status_code=409,
        detail=f"Please finish activity {active_activity.id} started_at: {active_activity.started_at} before starting another.",
    )

@router.patch(
    "/{activity_id}/finish",
    response_model=schemas.WorkoutActivityResponse,
)
def finish_workout_activity(
    workout_id: int,
    activity_id: int,
    ended_at_time: schemas.WorkoutActivityFinish,
    db: Session = Depends(get_db),
):
    workout = db.get(models.Workout, workout_id)

    if workout is None:
        raise HTTPException(
            status_code=404,
            detail="Workout not found",
        )

    activity_object = db.get(models.WorkoutActivity, activity_id)

    if (
        activity_object is None
        or activity_object.workout_id != workout_id
    ):
        raise HTTPException(
            status_code=404,
            detail="Activity not found in this workout",
        )
    if (ended_at_time.ended_at <= activity_object.started_at):
        raise HTTPException(
            status_code=422,
            detail="Cannot update finish time before starting time."
        )

    activity_object.ended_at = ended_at_time.ended_at
    db.commit()
    db.refresh(activity_object)

    return activity_object

# @router.get("", response_model=list[schemas.WorkoutActivityResponse])
# def get_workout_activities(
#     id: int,
#     db: Session = Depends(get_db),
# ):
#     statement = db.get(models.WorkoutActivity, id)

#     if statement is None:
#         raise HTTPException(status_code= 404, detail="it doesn't exist")

#     return db.scalars(statement).all()
#     # 1. Find the workout; return 404 if it doesn't exist.

#     # 2. Select activities where workout_id matches id.

#     # 3. Order by the activity's started_at.

#     # 4. Return all matching activities