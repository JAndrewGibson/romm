"""Add user preferences for playtime and friends

Revision ID: 0074_user_preferences
Revises: 0073_add_play_time_ms
Create Date: 2026-04-05 21:45:00.000000

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "0081_user_preferences"
down_revision = "0080_add_play_time_ms"
branch_labels = None
depends_on = None


def upgrade() -> None:
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    columns = [c["name"] for c in inspector.get_columns("users")]
    
    with op.batch_alter_table("users") as batch_op:
        if "playtime_tracking_enabled" not in columns:
            batch_op.add_column(
                sa.Column(
                    "playtime_tracking_enabled",
                    sa.Boolean(),
                    nullable=False,
                    server_default="1"
                )
            )
        if "friends_tab_visible" not in columns:
            batch_op.add_column(
                sa.Column(
                    "friends_tab_visible",
                    sa.Boolean(),
                    nullable=False,
                    server_default="1"
                )
            )


def downgrade() -> None:
    with op.batch_alter_table("users") as batch_op:
        batch_op.drop_column("playtime_tracking_enabled")
        batch_op.drop_column("friends_tab_visible")
