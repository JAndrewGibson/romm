"""Add play_time_ms to rom_user

Revision ID: 0073_add_play_time_ms
Revises: 0072_client_tokens
Create Date: 2026-04-05 20:18:00.000000

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "0073_add_play_time_ms"
down_revision = "0072_client_tokens"
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("rom_user") as batch_op:
        batch_op.add_column(
            sa.Column(
                "play_time_ms", 
                sa.BigInteger(), 
                nullable=False, 
                server_default="0"
            )
        )


def downgrade() -> None:
    with op.batch_alter_table("rom_user") as batch_op:
        batch_op.drop_column("play_time_ms")
