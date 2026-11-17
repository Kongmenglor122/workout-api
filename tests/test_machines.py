from app import models


def test_create_machine(client, db_session):
    payload = {
        "name": "Chest Press",
        "muscle_group": "Chest",
        "description": "Seated chest press machine",
    }

    response = client.post("/machines", json=payload)

    assert response.status_code == 201, response.text

    data = response.json()

    assert isinstance(data["id"], int)
    assert data["name"] == payload["name"]
    assert data["muscle_group"] == payload["muscle_group"]
    assert data["description"] == payload["description"]

    saved_machine = db_session.get(models.Machine, data["id"])
    assert saved_machine is not None
    assert saved_machine.name == payload["name"]
    assert saved_machine.muscle_group == payload["muscle_group"]
    assert saved_machine.description == payload["description"]