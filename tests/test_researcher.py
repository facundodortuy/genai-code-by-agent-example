"""Unit tests for the Researcher Agent."""
import pytest

from src.agents.researcher import ResearcherAgent
from src.models import ResearchTopic


@pytest.mark.asyncio
async def test_researcher_initialization():
    """Test that Researcher agent initializes correctly."""
    researcher = ResearcherAgent()
    assert researcher.name == "Researcher"
    assert researcher.role == "Academic AI Research Specialist"
    assert researcher.agent_id is not None


@pytest.mark.asyncio
async def test_researcher_process_machine_learning():
    """Test researcher processes machine learning topic correctly."""
    researcher = ResearcherAgent()
    topic = ResearchTopic(
        id="test-1",
        topic="Machine Learning Applications",
        keywords=["deep learning", "neural networks"]
    )

    finding = await researcher.process(topic)

    assert finding.topic_id == "test-1"
    assert "Machine Learning" in finding.title
    assert len(finding.summary) > 0
    assert len(finding.key_points) >= 4
    assert len(finding.sources) >= 3
    assert 0.0 <= finding.relevance_score <= 1.0


@pytest.mark.asyncio
async def test_researcher_process_nlp():
    """Test researcher processes NLP topic correctly."""
    researcher = ResearcherAgent()
    topic = ResearchTopic(
        id="test-2",
        topic="Natural Language Processing Advances",
        keywords=["transformers", "LLM"]
    )

    finding = await researcher.process(topic)

    assert finding.topic_id == "test-2"
    assert any(term in finding.title.lower() for term in ["nlp", "natural language"])
    assert len(finding.sources) >= 3
    assert finding.relevance_score > 0.8  # NLP topics tend to have high relevance


@pytest.mark.asyncio
async def test_researcher_process_generic_topic():
    """Test researcher handles generic AI topics."""
    researcher = ResearcherAgent()
    topic = ResearchTopic(
        id="test-3",
        topic="AI Safety Research",
        keywords=["alignment", "robustness"]
    )

    finding = await researcher.process(topic)

    assert finding.topic_id == "test-3"
    assert "Artificial Intelligence" in finding.title
    assert len(finding.key_points) >= 4
    assert finding.relevance_score >= 0.8
