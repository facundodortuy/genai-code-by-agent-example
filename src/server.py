"""FastMCP server for exposing the AI research agents system."""
import uuid
from typing import List

from fastmcp import FastMCP
from src.models import ResearchTopic
from src.orchestrator import ResearchOrchestrator

# Initialize FastMCP server
mcp = FastMCP("AI Research Agents")

# Initialize orchestrator
orchestrator = ResearchOrchestrator(approval_threshold=0.7)


@mcp.tool()
async def research_topic(topic: str, keywords: List[str] = None) -> dict:
    """Research an AI topic using the three-agent system.
    
    This tool coordinates the Researcher, Curator, and Editor agents to
    investigate an academic AI topic and produce a reviewed research report.
    
    Args:
        topic: The AI research topic to investigate
        keywords: Optional list of related keywords
        
    Returns:
        Complete research report with findings, curation, and editorial decision
    """
    # Create research topic
    research_topic = ResearchTopic(
        id=str(uuid.uuid4()),
        topic=topic,
        keywords=keywords or []
    )
    
    # Execute research workflow
    report = await orchestrator.research_topic(research_topic)
    
    # Return comprehensive results
    return {
        "topic": topic,
        "status": report.final_status.value,
        "finding": {
            "title": report.finding.title,
            "summary": report.finding.summary,
            "key_points": report.finding.key_points,
            "sources": report.finding.sources,
            "relevance_score": report.finding.relevance_score
        },
        "curation": {
            "quality_score": report.curated.quality_score,
            "categories": report.curated.categorization,
            "recommendations": report.curated.recommendations
        },
        "editorial_decision": {
            "decision": report.decision.decision,
            "reasoning": report.decision.reasoning,
            "final_score": report.decision.final_score,
            "improvements_needed": report.decision.improvements_needed
        }
    }


@mcp.tool()
async def research_multiple_topics(topics: List[str]) -> dict:
    """Research multiple AI topics in sequence.
    
    Args:
        topics: List of AI research topics
        
    Returns:
        Summary of all research reports
    """
    # Create research topics
    research_topics = [
        ResearchTopic(
            id=str(uuid.uuid4()),
            topic=topic,
            keywords=[]
        )
        for topic in topics
    ]
    
    # Execute research for all topics
    reports = await orchestrator.research_multiple_topics(research_topics)
    
    # Summarize results
    return {
        "total_topics": len(reports),
        "approved": len([r for r in reports if r.final_status.value == "approved"]),
        "rejected": len([r for r in reports if r.final_status.value == "rejected"]),
        "reports": [
            {
                "topic": r.topic.topic,
                "status": r.final_status.value,
                "quality_score": r.curated.quality_score,
                "final_score": r.decision.final_score
            }
            for r in reports
        ]
    }


@mcp.tool()
def get_research_statistics() -> dict:
    """Get statistics about all research conducted.
    
    Returns:
        Statistics including approval rates and average scores
    """
    return orchestrator.get_statistics()


@mcp.tool()
def get_approved_research() -> dict:
    """Get all approved research reports.
    
    Returns:
        List of approved research with summaries
    """
    reports = orchestrator.get_approved_reports()
    
    return {
        "count": len(reports),
        "reports": [
            {
                "topic": r.topic.topic,
                "title": r.finding.title,
                "summary": r.finding.summary,
                "categories": r.curated.categorization,
                "quality_score": r.curated.quality_score,
                "final_score": r.decision.final_score
            }
            for r in reports
        ]
    }


@mcp.tool()
def get_rejected_research() -> dict:
    """Get all rejected research reports with improvement suggestions.
    
    Returns:
        List of rejected research with reasons and improvements needed
    """
    reports = orchestrator.get_rejected_reports()
    
    return {
        "count": len(reports),
        "reports": [
            {
                "topic": r.topic.topic,
                "title": r.finding.title,
                "rejection_reason": r.decision.reasoning,
                "improvements_needed": r.decision.improvements_needed,
                "quality_score": r.curated.quality_score,
                "final_score": r.decision.final_score
            }
            for r in reports
        ]
    }


@mcp.resource("research://reports")
def list_all_reports() -> str:
    """Resource providing access to all research reports."""
    reports = orchestrator.get_all_reports()
    
    if not reports:
        return "No research reports available yet. Use research_topic() to start researching."
    
    output = "# AI Research Reports\n\n"
    output += f"Total Reports: {len(reports)}\n\n"
    
    for report in reports:
        output += f"## {report.topic.topic}\n"
        output += f"- **Status**: {report.final_status.value.upper()}\n"
        output += f"- **Quality Score**: {report.curated.quality_score:.2f}\n"
        output += f"- **Final Score**: {report.decision.final_score:.2f}\n"
        output += f"- **Decision**: {report.decision.decision}\n"
        output += f"- **Categories**: {', '.join(report.curated.categorization)}\n"
        output += "\n"
    
    return output


@mcp.resource("research://approved")
def list_approved_reports() -> str:
    """Resource providing access to approved research reports."""
    reports = orchestrator.get_approved_reports()
    
    if not reports:
        return "No approved research reports yet."
    
    output = "# Approved AI Research\n\n"
    
    for report in reports:
        output += f"## {report.finding.title}\n\n"
        output += f"**Topic**: {report.topic.topic}\n\n"
        output += f"{report.finding.summary}\n\n"
        output += "**Key Points**:\n"
        for point in report.finding.key_points:
            output += f"- {point}\n"
        output += "\n"
        output += f"**Quality Score**: {report.curated.quality_score:.2f}\n"
        output += f"**Categories**: {', '.join(report.curated.categorization)}\n\n"
        output += "---\n\n"
    
    return output


@mcp.prompt()
def research_prompt(topic: str) -> str:
    """Generate a prompt for researching an AI topic.
    
    Args:
        topic: The AI topic to research
        
    Returns:
        Formatted prompt
    """
    return f"""I need comprehensive academic research on the following AI topic:

Topic: {topic}

Please use the research_topic() tool to:
1. Have the Researcher agent investigate the topic
2. Have the Curator agent organize and assess the findings
3. Have the Editor agent make a publication decision

The system will coordinate all three agents and provide a complete report including:
- Research findings with academic sources
- Quality assessment and categorization
- Editorial decision with reasoning

After receiving the results, you can:
- Use get_approved_research() to see approved content
- Use get_research_statistics() to see overall metrics
- Research additional related topics for comprehensive coverage
"""


@mcp.prompt()
def batch_research_prompt(topics: List[str]) -> str:
    """Generate a prompt for researching multiple AI topics.
    
    Args:
        topics: List of AI topics to research
        
    Returns:
        Formatted prompt
    """
    topics_formatted = "\n".join(f"{i+1}. {topic}" for i, topic in enumerate(topics))
    
    return f"""I need to research multiple AI topics systematically:

{topics_formatted}

Use research_multiple_topics() with these topics to:
- Process each topic through the three-agent workflow
- Get comprehensive reports for all topics
- Receive a summary with approval statistics

After completion, you can:
- Review approved content with get_approved_research()
- Check rejected content and improvements with get_rejected_research()
- Analyze overall statistics with get_research_statistics()
"""


if __name__ == "__main__":
    # Run the MCP server
    mcp.run()
