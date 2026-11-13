from sqlalchemy import create_engine

from app.config import settings

from sqlalchemy.orm import DeclarativeBase, sessionmaker

engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
)


SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass


def get_db():
    with SessionLocal() as db:
        yield db