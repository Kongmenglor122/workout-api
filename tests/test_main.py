def test_root(client):
    response = client.get("/")

    assert response.status_code == 201
    assert response.json() == {
        "message": "Welcome to your Workout API"
    }