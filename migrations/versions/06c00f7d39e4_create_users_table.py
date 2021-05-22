"""create table

Revision ID: 06c00f7d39e4
Revises: 
Create Date: 2021-05-21 21:56:15.511772

"""
from uuid import uuid4
from datetime import datetime, timedelta
from alembic import op
from sqlalchemy.dialects.postgresql import UUID
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '06c00f7d39e4'
down_revision = None
branch_labels = None
depends_on = None

UTC_NOW = datetime.utcnow()
KST     = timedelta(hours=9)
KOR_NOW = UTC_NOW + KST


def upgrade():
    op.create_table(
        'users',
        sa.Column('user_id', sa.Integer(), autoincrement=True, primary_key=True),
    )

    op.create_table(
        'study_rooms',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid4),
        sa.Column('title', sa.String(64), nullable=False),
        sa.Column('description', sa.String(256), nullable=False),
        sa.Column('is_public', sa.Boolean(), nullable=False),
        sa.Column('password', sa.String(32), nullable=True),
        sa.Column('current_join_counts', sa.SmallInteger(), nullable=False, default=0),
        sa.Column('created_at', sa.DateTime(), default=KOR_NOW, nullable=False),
        sa.Column('owner_id', sa.Integer(), sa.ForeignKey('users.user_id', ondelete='CASCADE')),
    )

    op.create_table(
        'reports',
        sa.Column('id', sa.Integer(), autoincrement=True, primary_key=True),
        sa.Column('report_date', sa.Date, nullable=False),
        sa.Column('achivement', sa.Integer(), nullable=False),
        sa.Column('concentration', sa.Integer(), nullable=False),
        sa.Column('total_time', sa.Integer(), nullable=False),
        sa.Column('total_star_count', sa.Integer(), nullable=False),
        sa.Column('total_disturbance', sa.ARRAY(sa.JSON), nullable=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.user_id', ondelete='CASCADE')),
    )

    op.create_table(
        'my_studies',
        sa.Column('id', sa.Integer(), autoincrement=True, primary_key=True),
        sa.Column('study_date', sa.Date, nullable=False),
        sa.Column('started_at', sa.TIMESTAMP, nullable=False),
        sa.Column('ended_at', sa.TIMESTAMP, nullable=False),
        sa.Column('total_time', sa.Integer(), nullable=False),
        sa.Column('star_count', sa.Integer, nullable=True),
        sa.Column('disturbance', sa.ARRAY(sa.JSON), nullable=True),
        sa.Column('report_id', sa.Integer(), sa.ForeignKey('reports.id', ondelete='CASCADE')),
        sa.Column('study_room_id', UUID(), sa.ForeignKey('study_rooms.id', ondelete='CASCADE'))
    )
    


def downgrade():
    op.drop_table('users')
    op.drop_table('study_rooms')
    op.drop_table('my_studies')
    op.drop_table('reports')
