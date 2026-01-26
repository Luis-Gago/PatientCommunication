#!/usr/bin/env python3
"""
Test script for medication adherence analysis
"""
import asyncio
import sys
import os
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.base import SessionLocal
from app.services.medication_analysis_service import medication_analysis_service
import json


async def test_analysis():
    """Test medication adherence analysis"""
    db = SessionLocal()
    
    try:
        # Test parameters
        research_id = input("Enter research ID to analyze (e.g., PACO-001): ").strip()
        
        print(f"\n🔍 Analyzing conversations for {research_id}...")
        
        # Get conversation transcript first
        try:
            transcript, count, earliest, latest = (
                medication_analysis_service.get_conversation_transcript(
                    db=db,
                    research_id=research_id
                )
            )
            
            print(f"\n📊 Found {count} messages")
            print(f"📅 Date range: {earliest.strftime('%Y-%m-%d')} to {latest.strftime('%Y-%m-%d')}")
            print(f"\n📝 Transcript preview (first 500 chars):")
            print(transcript[:500])
            print("...\n")
            
        except ValueError as e:
            print(f"❌ Error: {e}")
            return
        
        # Ask if user wants to proceed
        proceed = input("Proceed with analysis? (y/n): ").strip().lower()
        if proceed != 'y':
            print("Analysis cancelled.")
            return
        
        # Perform analysis
        print("\n🤖 Running NLP analysis (this may take 30-60 seconds)...")
        
        analysis = await medication_analysis_service.analyze_medication_adherence(
            db=db,
            research_id=research_id,
            model="gpt-4o"
        )
        
        print(f"\n✅ Analysis complete!")
        print(f"Analysis ID: {analysis.id}")
        print(f"Confidence Score: {analysis.confidence_score}%")
        print(f"\n📋 Summary:")
        print(analysis.summary)
        
        # Parse detailed results
        try:
            detailed = json.loads(analysis.detailed_analysis)
            
            print(f"\n💊 Medications ({len(detailed.get('medications', []))}):")
            for med in detailed.get('medications', []):
                dosage = med.get('dosage', 'dosage not mentioned')
                print(f"  • {med['name']} - {dosage}")
            
            print(f"\n⚠️ Side Effects ({len(detailed.get('side_effects', []))}):")
            for se in detailed.get('side_effects', []):
                print(f"  • {se['medication']}: {se['effect']} ({se['severity']})")
            
            print(f"\n🚧 Adherence Difficulties ({len(detailed.get('adherence_difficulties', []))}):")
            for diff in detailed.get('adherence_difficulties', []):
                print(f"  • [{diff['type']}] {diff['description']}")
            
            print(f"\n✨ Adherence Strategies ({len(detailed.get('adherence_strategies', []))}):")
            for strat in detailed.get('adherence_strategies', []):
                print(f"  • [{strat['type']}] {strat['description']} - {strat['effectiveness']}")
            
            print(f"\n❓ Questions/Concerns ({len(detailed.get('questions_concerns', []))}):")
            for qc in detailed.get('questions_concerns', []):
                status = "✓" if qc['addressed'] else "✗"
                print(f"  {status} [{qc['topic']}] {qc['question']}")
            
            print(f"\n🎯 Key Concerns:")
            for concern in detailed.get('key_concerns', []):
                print(f"  • {concern}")
            
            print(f"\n💡 Recommendations:")
            for rec in detailed.get('recommendations', []):
                print(f"  • {rec}")
            
            print(f"\n📈 Overall Adherence:")
            oa = detailed.get('overall_adherence', {})
            print(f"  Taking medications: {oa.get('taking_medications', 'unclear')}")
            print(f"  Taking as prescribed: {oa.get('taking_as_prescribed', 'unclear')}")
            print(f"  Taking correct medications: {oa.get('taking_correct_medications', 'unclear')}")
            
        except json.JSONDecodeError:
            print("\n⚠️ Could not parse detailed analysis")
            print("Raw analysis:")
            print(analysis.detailed_analysis[:500])
        
    finally:
        db.close()


def test_history():
    """Test getting analysis history"""
    db = SessionLocal()
    
    try:
        research_id = input("Enter research ID: ").strip()
        
        analyses = medication_analysis_service.get_analysis_history(
            db=db,
            research_id=research_id,
            limit=10
        )
        
        if not analyses:
            print(f"No analyses found for {research_id}")
            return
        
        print(f"\n📚 Analysis History for {research_id}:")
        print(f"{'ID':<8} {'Date':<20} {'Messages':<10} {'Confidence':<12} {'Summary':<50}")
        print("-" * 100)
        
        for a in analyses:
            date_str = a.analysis_date.strftime("%Y-%m-%d %H:%M")
            summary_preview = a.summary[:47] + "..." if len(a.summary) > 50 else a.summary
            print(f"{a.id:<8} {date_str:<20} {a.conversation_count:<10} {a.confidence_score}%{'':<8} {summary_preview:<50}")
        
    finally:
        db.close()


def main():
    """Main menu"""
    print("=" * 60)
    print("Medication Adherence Analysis Test Tool")
    print("=" * 60)
    print("\nOptions:")
    print("1. Run new analysis")
    print("2. View analysis history")
    print("3. Exit")
    
    choice = input("\nSelect option (1-3): ").strip()
    
    if choice == '1':
        asyncio.run(test_analysis())
    elif choice == '2':
        test_history()
    elif choice == '3':
        print("Goodbye!")
    else:
        print("Invalid option")


if __name__ == "__main__":
    main()
