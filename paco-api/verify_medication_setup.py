#!/usr/bin/env python3
"""
Quick test to verify the medication analysis system is working
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.base import engine
import sqlalchemy as sa

def verify_setup():
    """Verify database setup"""
    print("🔍 Verifying Medication Analysis Setup\n")
    print("=" * 60)
    
    # Check table exists
    inspector = sa.inspect(engine)
    tables = inspector.get_table_names()
    
    print("\n1. Database Tables:")
    for table in sorted(tables):
        marker = "✅" if table in ['paco_medication_adherence', 'paco_conversations', 'paco_research_ids'] else "  "
        print(f"   {marker} {table}")
    
    if 'paco_medication_adherence' not in tables:
        print("\n❌ ERROR: paco_medication_adherence table not found!")
        return False
    
    print("\n   ✅ All required tables present")
    
    # Check indexes
    print("\n2. Table Indexes:")
    with engine.connect() as conn:
        result = conn.execute(sa.text("""
            SELECT indexname 
            FROM pg_indexes 
            WHERE tablename = 'paco_medication_adherence'
        """))
        indexes = [row[0] for row in result]
        
        for idx in indexes:
            print(f"   ✅ {idx}")
    
    # Check columns
    print("\n3. Table Columns:")
    columns = inspector.get_columns('paco_medication_adherence')
    required_cols = [
        'id', 'research_id_fk', 'analysis_date', 'analyzed_from', 
        'analyzed_to', 'conversation_count', 'is_taking_medications',
        'adherence_barriers', 'side_effects', 'medication_list',
        'confidence_score', 'summary', 'detailed_analysis', 'model_used'
    ]
    
    col_names = [col['name'] for col in columns]
    for col in required_cols:
        if col in col_names:
            print(f"   ✅ {col}")
        else:
            print(f"   ❌ {col} - MISSING!")
    
    # Check research IDs exist
    print("\n4. Research IDs:")
    with engine.connect() as conn:
        result = conn.execute(sa.text("""
            SELECT research_id, is_active 
            FROM paco_research_ids 
            ORDER BY created_at DESC 
            LIMIT 5
        """))
        research_ids = list(result)
        
        if research_ids:
            for rid, active in research_ids:
                status = "✅ Active" if active else "⚠️  Inactive"
                print(f"   {status} {rid}")
        else:
            print("   ⚠️  No research IDs found - you'll need to create some first")
    
    # Check for conversations
    print("\n5. Conversation Data:")
    with engine.connect() as conn:
        result = conn.execute(sa.text("""
            SELECT COUNT(*) as total, 
                   COUNT(DISTINCT research_id_fk) as unique_patients,
                   COUNT(DISTINCT conversation_id) as unique_conversations
            FROM paco_conversations
        """))
        stats = result.fetchone()
        
        if stats and stats[0] > 0:
            print(f"   ✅ {stats[0]:,} total messages")
            print(f"   ✅ {stats[1]} patients with conversations")
            print(f"   ✅ {stats[2]} unique conversations")
        else:
            print("   ⚠️  No conversations found yet")
    
    # Check API imports
    print("\n6. API Components:")
    try:
        from app.services.medication_analysis_service import medication_analysis_service
        print("   ✅ medication_analysis_service")
    except ImportError as e:
        print(f"   ❌ medication_analysis_service - {e}")
        return False
    
    try:
        from app.api.endpoints import medication_analysis
        print("   ✅ medication_analysis endpoints")
    except ImportError as e:
        print(f"   ❌ medication_analysis endpoints - {e}")
        return False
    
    try:
        from app.schemas.medication_analysis import AnalysisRequest, AnalysisResponse
        print("   ✅ medication_analysis schemas")
    except ImportError as e:
        print(f"   ❌ medication_analysis schemas - {e}")
        return False
    
    # Check environment
    print("\n7. Environment Configuration:")
    from app.core.config import get_settings
    settings = get_settings()
    
    if settings.OPENAI_API_KEY:
        print("   ✅ OPENAI_API_KEY configured")
    else:
        print("   ⚠️  OPENAI_API_KEY not set")
    
    if settings.ADMIN_PASSWORD:
        print("   ✅ ADMIN_PASSWORD configured")
    else:
        print("   ⚠️  ADMIN_PASSWORD not set")
    
    print("\n" + "=" * 60)
    print("✅ Setup verification complete!\n")
    
    print("Next steps:")
    print("1. Start the API server: uvicorn app.main:app --reload")
    print("2. Visit http://localhost:8000/docs")
    print("3. Look for 'medication-analysis' section")
    print("4. Use POST /api/v1/medication-analysis/analyze")
    print("\nOr test with: python test_medication_analysis.py")
    
    return True

if __name__ == "__main__":
    try:
        verify_setup()
    except Exception as e:
        print(f"\n❌ Error during verification: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
