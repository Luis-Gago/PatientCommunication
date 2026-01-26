"""Add medication adherence analysis table

Revision ID: a5bc8d3e4f2g
Revises: 694a65473b3d
Create Date: 2025-01-26 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a5bc8d3e4f2g'
down_revision = '694a65473b3d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create medication adherence analysis table
    op.execute("""
        CREATE TABLE IF NOT EXISTS paco_medication_adherence (
            id SERIAL PRIMARY KEY,
            research_id_fk INTEGER NOT NULL REFERENCES paco_research_ids(id),
            
            -- Analysis metadata
            analysis_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            analyzed_from TIMESTAMP WITH TIME ZONE NOT NULL,
            analyzed_to TIMESTAMP WITH TIME ZONE NOT NULL,
            conversation_count INTEGER DEFAULT 0,
            
            -- Medication adherence findings
            is_taking_medications BOOLEAN,
            taking_as_prescribed BOOLEAN,
            taking_correct_medications BOOLEAN,
            
            -- Detailed insights (stored as text for provider review)
            adherence_barriers TEXT,
            adherence_strategies TEXT,
            side_effects TEXT,
            medication_list TEXT,
            
            -- Confidence and summary
            confidence_score INTEGER DEFAULT 0,
            summary TEXT NOT NULL,
            detailed_analysis TEXT,
            
            -- Model tracking
            model_used VARCHAR(100)
        )
    """)
    
    # Create indexes
    op.execute("""
        CREATE INDEX IF NOT EXISTS ix_adherence_research_date 
        ON paco_medication_adherence(research_id_fk, analysis_date)
    """)
    
    op.execute("""
        CREATE INDEX IF NOT EXISTS ix_adherence_analysis_date 
        ON paco_medication_adherence(analysis_date)
    """)


def downgrade() -> None:
    # Drop table and indexes
    op.execute("DROP TABLE IF EXISTS paco_medication_adherence")
