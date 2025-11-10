"""Orchestrator for coordinating the three AI agents."""
from typing import Dict, List
from src.agents import CuratorAgent, EditorAgent, ResearcherAgent
from src.models import (
    EditorialDecision,
    ResearchReport,
    ResearchStatus,
    ResearchTopic,
)


class ResearchOrchestrator:
    """Orchestrates the workflow between Researcher, Curator, and Editor agents."""
    
    def __init__(self, approval_threshold: float = 0.7):
        """Initialize the orchestrator with all three agents.
        
        Args:
            approval_threshold: Minimum score for Editor approval
        """
        self.researcher = ResearcherAgent()
        self.curator = CuratorAgent()
        self.editor = EditorAgent(approval_threshold=approval_threshold)
        self.reports: Dict[str, ResearchReport] = {}
    
    async def research_topic(self, topic: ResearchTopic) -> ResearchReport:
        """Execute the complete research workflow for a topic.
        
        Args:
            topic: Research topic to investigate
            
        Returns:
            Complete research report with all stages
        """
        print(f"\n{'='*80}")
        print(f"Starting research workflow for: {topic.topic}")
        print(f"{'='*80}\n")
        
        # Stage 1: Research
        finding = await self.researcher.process(topic)
        
        # Stage 2: Curation
        curated = await self.curator.process(finding)
        
        # Stage 3: Editorial Decision
        decision = await self.editor.process(curated)
        
        # Determine final status
        final_status = (
            ResearchStatus.APPROVED if decision.decision == "approved"
            else ResearchStatus.REJECTED
        )
        
        # Create comprehensive report
        report = ResearchReport(
            topic=topic,
            finding=finding,
            curated=curated,
            decision=decision,
            final_status=final_status
        )
        
        # Store report
        self.reports[report.topic.id] = report
        
        print(f"\n{'='*80}")
        print(f"Workflow complete: {final_status.value.upper()}")
        print(f"Final Score: {decision.final_score:.2f}")
        print(f"{'='*80}\n")
        
        return report
    
    async def research_multiple_topics(self, topics: List[ResearchTopic]) -> List[ResearchReport]:
        """Research multiple topics sequentially.
        
        Args:
            topics: List of research topics
            
        Returns:
            List of research reports
        """
        reports = []
        for topic in topics:
            report = await self.research_topic(topic)
            reports.append(report)
        
        return reports
    
    def get_report(self, topic_id: str) -> ResearchReport | None:
        """Get a research report by topic ID.
        
        Args:
            topic_id: Topic ID
            
        Returns:
            Research report or None if not found
        """
        return self.reports.get(topic_id)
    
    def get_all_reports(self) -> List[ResearchReport]:
        """Get all research reports.
        
        Returns:
            List of all research reports
        """
        return list(self.reports.values())
    
    def get_approved_reports(self) -> List[ResearchReport]:
        """Get only approved research reports.
        
        Returns:
            List of approved research reports
        """
        return [
            report for report in self.reports.values()
            if report.final_status == ResearchStatus.APPROVED
        ]
    
    def get_rejected_reports(self) -> List[ResearchReport]:
        """Get only rejected research reports.
        
        Returns:
            List of rejected research reports
        """
        return [
            report for report in self.reports.values()
            if report.final_status == ResearchStatus.REJECTED
        ]
    
    def get_statistics(self) -> Dict[str, any]:
        """Get statistics about the research process.
        
        Returns:
            Dictionary with statistics
        """
        total = len(self.reports)
        approved = len(self.get_approved_reports())
        rejected = len(self.get_rejected_reports())
        
        avg_quality = (
            sum(r.curated.quality_score for r in self.reports.values()) / total
            if total > 0 else 0.0
        )
        
        avg_final = (
            sum(r.decision.final_score for r in self.reports.values()) / total
            if total > 0 else 0.0
        )
        
        return {
            "total_reports": total,
            "approved": approved,
            "rejected": rejected,
            "approval_rate": approved / total if total > 0 else 0.0,
            "average_quality_score": avg_quality,
            "average_final_score": avg_final
        }
