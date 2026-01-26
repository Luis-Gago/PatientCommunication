#!/usr/bin/env python3
"""
Manually create the medication adherence table
This bypasses Alembic due to version mismatch
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.base import engine
import sqlalchemy as sa

def create_medication_adherence_table():
    """Create the paco_medication_adherence table"""
    
    # Check if table exists
    inspector = sa.inspect(engine)
    if 'paco_medication_adherence' in inspector.get_table_names():
        print("✅ Table paco_medication_adherence already exists")
        return
    
    print("🔧 Creating paco_medication_adherence table...")
    
    with engine.connect() as conn:
        # Create table
        conn.execute(sa.text("""
            CREATE TABLE paco_medication_adherence (
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
        """))
        
        print("✅ Table created successfully")
        
        # Create indexes
        print("🔧 Creating indexes...")
        
        conn.execute(sa.text("""
            CREATE INDEX IF NOT EXISTS ix_adherence_research_date 
            ON paco_medication_adherence(research_id_fk, analysis_date)
        """))
        
        conn.execute(sa.text("""
            CREATE INDEX IF NOT EXISTS ix_adherence_analysis_date 
            ON paco_medication_adherence(analysis_date)
        """))
        
        conn.commit()
        print("✅ Indexes created successfully")
    
    print("\n✅ Medication adherence table setup complete!")
    print("\nYou can now use the medication analysis API endpoints.")

if __name__ == "__main__":
    try:
        create_medication_adherence_table()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
