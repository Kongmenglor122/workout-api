"""Add workout ownership

Revision ID: 777d9f962c32
Revises: af6140f9681d
Create Date: 2026-11-17 10:42:52.080843

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '777d9f962c32'
down_revision: Union[str, Sequence[str], None] = 'af6140f9681d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Allow existing rows to temporarily have no owner.
    op.add_column(
        "workouts",
        sa.Column("user_id", sa.Integer(), nullable=True),
    )

    # Assign existing workouts to your local account.
    op.execute(
        sa.text(
            "UPDATE workouts SET user_id = 2 "
            "WHERE user_id IS NULL"
        )
    )

    op.create_foreign_key(
        "fk_workouts_user_id_users",
        "workouts",
        "users",
        ["user_id"],
        ["id"],
    )

    op.alter_column(
        "workouts",
        "user_id",
        existing_type=sa.Integer(),
        nullable=False,
    )


def downgrade() -> None:
    op.drop_constraint(
        "fk_workouts_user_id_users",
        "workouts",
        type_="foreignkey",
    )

    op.drop_column("workouts", "user_id")