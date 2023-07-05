from alembic import op
import sqlalchemy as sa


# Declare the revision variable
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'videos',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.String(100), index=True),
        sa.Column('description', sa.String(500)),
        sa.Column('duration', sa.Integer)
    )


def downgrade():
    op.drop_table('videos')
