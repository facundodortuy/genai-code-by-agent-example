"""Unit tests for the Research Orchestrator."""
import pytest

from src.models import ResearchStatus, ResearchTopic
from src.orchestrator import ResearchOrchestrator


@pytest.mark.asyncio
async def test_orchestrator_initialization():
    """Test that orchestrator initializes correctly."""
    orchestrator = ResearchOrchestrator(approval_threshold=0.7)
    assert orchestrator.researcher is not None
    assert orchestrator.curator is not None
    assert orchestrator.editor is not None
    assert len(orchestrator.reports) == 0


@pytest.mark.asyncio
async def test_orchestrator_research_topic():
    """Test orchestrator processes a research topic through all agents."""
    orchestrator = ResearchOrchestrator(approval_threshold=0.7)

    topic = ResearchTopic(
        id="test-topic-1",
        topic="Machine Learning Applications",
        keywords=["deep learning"]
    )

    report = await orchestrator.research_topic(topic)

    assert report.topic.id == "test-topic-1"
    assert report.finding is not None
    assert report.curated is not None
    assert report.decision is not None
    assert report.final_status in [ResearchStatus.APPROVED, ResearchStatus.REJECTED]


@pytest.mark.asyncio
async def test_orchestrator_multiple_topics():
    """Test orchestrator processes multiple topics."""
    orchestrator = ResearchOrchestrator(approval_threshold=0.7)

    topics = [
        ResearchTopic(
            id=f"topic-{i}",
            topic=f"AI Research Topic {i}",
            keywords=["AI"]
        )
        for i in range(3)
    ]

    reports = await orchestrator.research_multiple_topics(topics)

    assert len(reports) == 3
    assert len(orchestrator.reports) == 3
    for report in reports:
        assert report.final_status in [ResearchStatus.APPROVED, ResearchStatus.REJECTED]


@pytest.mark.asyncio
async def test_orchestrator_get_statistics():
    """Test orchestrator statistics generation."""
    orchestrator = ResearchOrchestrator(approval_threshold=0.7)

    topics = [
        ResearchTopic(
            id=f"topic-{i}",
            topic=f"Machine Learning Topic {i}",
            keywords=["ML"]
        )
        for i in range(2)
    ]

    await orchestrator.research_multiple_topics(topics)

    stats = orchestrator.get_statistics()

    assert stats["total_reports"] == 2
    assert stats["approved"] + stats["rejected"] == 2
    assert 0.0 <= stats["approval_rate"] <= 1.0
    assert 0.0 <= stats["average_quality_score"] <= 1.0
    assert 0.0 <= stats["average_final_score"] <= 1.0


@pytest.mark.asyncio
async def test_orchestrator_get_approved_rejected():
    """Test orchestrator filtering of approved and rejected reports."""
    orchestrator = ResearchOrchestrator(approval_threshold=0.7)

    # Research multiple topics to get varied results
    topics = [
        ResearchTopic(
            id=f"topic-{i}",
            topic=f"NLP Research {i}",
            keywords=["NLP"]
        )
        for i in range(4)
    ]

    await orchestrator.research_multiple_topics(topics)

    approved = orchestrator.get_approved_reports()
    rejected = orchestrator.get_rejected_reports()

    assert len(approved) + len(rejected) == 4

    for report in approved:
        assert report.final_status == ResearchStatus.APPROVED

    for report in rejected:
        assert report.final_status == ResearchStatus.REJECTED
