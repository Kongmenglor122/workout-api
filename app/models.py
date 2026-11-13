from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Machine(Base):
    __tablename__ = "machines"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    muscle_group: Mapped[str] = mapped_column(String(50))
    description: Mapped[str | None] = mapped_column(String(500))