"""add owner_id to projects nullable

Revision ID: dd3f056272df
Revises: c2b8ecd180e0
Create Date: 2026-05-05 07:30:07.676093

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'dd3f056272df'
down_revision: Union[str, Sequence[str], None] = 'c2b8ecd180e0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column(
        'projects',
        sa.Column('owner_id', sa.Integer(), nullable=True)
    )
    op.create_foreign_key(
        'fk_projects_owner_id',
        'projects', 'users',
        ['owner_id'], ['id']
    )
    op.create_index(
        'ix_projects_owner_id',
        'projects',
        ['owner_id']
    )


def downgrade():
    op.drop_index('ix_projects_owner_id', table_name='projects')
    op.drop_constraint('fk_projects_owner_id', 'projects', type_='foreignkey')
    op.drop_column('projects', 'owner_id')
