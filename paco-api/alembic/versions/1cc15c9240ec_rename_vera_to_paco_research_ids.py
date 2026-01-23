"""rename_vera_to_paco_research_ids

Revision ID: 1cc15c9240ec
Revises: 694a65473b3d
Create Date: 2026-01-23 11:35:41.056029

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1cc15c9240ec'
down_revision = '694a65473b3d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Rename the table from vera_research_ids to paco_research_ids
    op.rename_table('vera_research_ids', 'paco_research_ids')
    
    # Rename the indexes
    op.execute('ALTER INDEX ix_vera_research_ids_id RENAME TO ix_paco_research_ids_id')
    op.execute('ALTER INDEX ix_vera_research_ids_research_id RENAME TO ix_paco_research_ids_research_id')
    
    # Update foreign key constraint names in dependent tables
    # Note: PostgreSQL doesn't require renaming FK constraints when table is renamed


def downgrade() -> None:
    # Reverse the changes
    op.execute('ALTER INDEX ix_paco_research_ids_research_id RENAME TO ix_vera_research_ids_research_id')
    op.execute('ALTER INDEX ix_paco_research_ids_id RENAME TO ix_vera_research_ids_id')
    
    op.rename_table('paco_research_ids', 'vera_research_ids')
