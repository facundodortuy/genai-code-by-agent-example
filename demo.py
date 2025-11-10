"""Demo script showing the AI research agents in action."""
import asyncio
import uuid
from src.models import ResearchTopic
from src.orchestrator import ResearchOrchestrator


async def main():
    """Run demo of the multi-agent research system."""
    print("\n" + "="*80)
    print("AI RESEARCH AGENTS - DEMO")
    print("Multi-Agent System for Academic AI Research")
    print("="*80 + "\n")
    
    # Initialize orchestrator
    orchestrator = ResearchOrchestrator(approval_threshold=0.7)
    
    # Define sample topics
    topics = [
        ResearchTopic(
            id=str(uuid.uuid4()),
            topic="Machine Learning in Healthcare",
            keywords=["deep learning", "medical imaging", "diagnosis"]
        ),
        ResearchTopic(
            id=str(uuid.uuid4()),
            topic="Natural Language Processing for Academic Research",
            keywords=["NLP", "text analysis", "research automation"]
        ),
        ResearchTopic(
            id=str(uuid.uuid4()),
            topic="Computer Vision Applications in Autonomous Vehicles",
            keywords=["object detection", "self-driving", "perception"]
        ),
        ResearchTopic(
            id=str(uuid.uuid4()),
            topic="Ethics and Bias in AI Systems",
            keywords=["fairness", "transparency", "responsible AI"]
        ),
    ]
    
    print(f"Researching {len(topics)} AI topics...\n")
    
    # Research all topics
    reports = await orchestrator.research_multiple_topics(topics)
    
    # Display results summary
    print("\n" + "="*80)
    print("RESEARCH SUMMARY")
    print("="*80 + "\n")
    
    for i, report in enumerate(reports, 1):
        print(f"{i}. {report.topic.topic}")
        print(f"   Status: {report.final_status.value.upper()}")
        print(f"   Quality: {report.curated.quality_score:.2f} | Final: {report.decision.final_score:.2f}")
        print(f"   Categories: {', '.join(report.curated.categorization)}")
        print()
    
    # Display statistics
    stats = orchestrator.get_statistics()
    print("="*80)
    print("STATISTICS")
    print("="*80)
    print(f"Total Reports: {stats['total_reports']}")
    print(f"Approved: {stats['approved']} ({stats['approval_rate']*100:.1f}%)")
    print(f"Rejected: {stats['rejected']}")
    print(f"Average Quality Score: {stats['average_quality_score']:.2f}")
    print(f"Average Final Score: {stats['average_final_score']:.2f}")
    print()
    
    # Display approved research details
    approved = orchestrator.get_approved_reports()
    if approved:
        print("="*80)
        print("APPROVED RESEARCH DETAILS")
        print("="*80 + "\n")
        
        for report in approved:
            print(f"Topic: {report.topic.topic}")
            print(f"Title: {report.finding.title}")
            print(f"\nSummary:")
            print(report.finding.summary)
            print(f"\nKey Points:")
            for point in report.finding.key_points:
                print(f"  • {point}")
            print(f"\nSources:")
            for source in report.finding.sources:
                print(f"  - {source}")
            print(f"\nEditor's Comment: {report.decision.reasoning}")
            print("\n" + "-"*80 + "\n")
    
    # Display rejected research with improvements
    rejected = orchestrator.get_rejected_reports()
    if rejected:
        print("="*80)
        print("REJECTED RESEARCH - IMPROVEMENTS NEEDED")
        print("="*80 + "\n")
        
        for report in rejected:
            print(f"Topic: {report.topic.topic}")
            print(f"Title: {report.finding.title}")
            print(f"\nRejection Reason: {report.decision.reasoning}")
            print(f"\nImprovements Needed:")
            for improvement in report.decision.improvements_needed:
                print(f"  • {improvement}")
            print("\n" + "-"*80 + "\n")
    
    print("="*80)
    print("DEMO COMPLETE")
    print("="*80)


if __name__ == "__main__":
    asyncio.run(main())
