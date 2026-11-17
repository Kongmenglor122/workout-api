from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.orm import sessionmaker

from app.config import settings

import pytest

from app import models
from app.database import Base

from fastapi.testclient import TestClient

from app.main import app
from app.database import get_db


test_database_url = make_url(settings.database_url).set(
    database="workout_test_db"
)

test_engine = create_engine(
    test_database_url,
    pool_pre_ping=True,
)

TestSessionLocal = sessionmaker(bind=test_engine)

@pytest.fixture
def db_session():
    if test_engine.url.database != "workout_test_db":
        raise RuntimeError("Tests must use workout_test_db")

    Base.metadata.create_all(bind=test_engine)

    with TestSessionLocal() as db:
        try:
            yield db
        finally:
            db.rollback()

    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.pop(get_db, None)