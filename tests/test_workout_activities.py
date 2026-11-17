from app import models
from datetime import datetime, timezone

from datetime import datetime, timezone


def test_create_workoutactivity(client):
    machine = {
        "name": "Chest Press",
        "muscle_group": "Chest",
        "description": "Seated chest press machine",
    }

    workout = {
        "started_at": datetime.now(timezone.utc).isoformat(),
        "notes": "Started working out",
    }

    machine_response = client.post("/machines", json=machine)
    assert machine_response.status_code == 201, machine_response.text

    workout_response = client.post("/workouts", json=workout)
    assert workout_response.status_code == 201, workout_response.text

    machine_id = machine_response.json()["id"]
    workout_id = workout_response.json()["id"]

    workout_activity = {
        "machine_id": machine_id,
        "started_at": workout_response.json()["started_at"],
    }

    activity_response = client.post(
        f"/workouts/{workout_id}/activities",
        params={"workout_id": workout_id},
        json=workout_activity,
    )

    assert activity_response.status_code == 201, activity_response.text

    data = activity_response.json()

    assert data["machine_id"] == machine_id
    assert data["workout_id"] == workout_id
    assert data["ended_at"] is None
