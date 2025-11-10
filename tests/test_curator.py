"""Unit tests for the Curator Agent."""
import pytest

from src.agents.curator import CuratorAgent
from src.models import ResearchFinding, ResearchStatus


@pytest.mark.asyncio
async def test_curator_initialization():
    """Test that Curator agent initializes correctly."""
    curator = CuratorAgent()
    assert curator.name == "Curator"
    assert curator.role == "Research Content Curator"
    assert curator.agent_id is not None


@pytest.mark.asyncio
async def test_curator_process_high_quality():
    """Test curator processes high-quality finding correctly."""
    curator = CuratorAgent()
    finding = ResearchFinding(
        id="finding-1",
        topic_id="topic-1",
        title="Machine Learning Advances",
        summary="A comprehensive study on recent ML advances with deep analysis",
        key_points=["Point 1", "Point 2", "Point 3", "Point 4"],
        sources=["Source 1", "Source 2", "Source 3", "Source 4"],
        relevance_score=0.9,
        status=ResearchStatus.PENDING
    )

    curated = await curator.process(finding)

    assert curated.finding_id == "finding-1"
    assert curated.quality_score >= 0.7
    assert len(curated.categorization) > 0
    assert len(curated.organized_summary) > 0
    assert curated.status == ResearchStatus.CURATED


@pytest.mark.asyncio
async def test_curator_assess_quality():
    """Test curator quality assessment."""
    curator = CuratorAgent()

    high_quality_finding = ResearchFinding(
        id="finding-2",
        topic_id="topic-2",
        title="NLP Research",
        summary="A detailed analysis of natural language processing with comprehensive coverage",
        key_points=["Point 1", "Point 2", "Point 3", "Point 4", "Point 5"],
        sources=["Source 1", "Source 2", "Source 3", "Source 4", "Source 5"],
        relevance_score=0.95,
        status=ResearchStatus.PENDING
    )

    quality = curator._assess_quality(high_quality_finding)
    assert quality >= 0.8


@pytest.mark.asyncio
async def test_curator_categorization():
    """Test curator categorization logic."""
    curator = CuratorAgent()

    finding = ResearchFinding(
        id="finding-3",
        topic_id="topic-3",
        title="Machine Learning and Natural Language Processing Integration",
        summary="Combining ML and NLP for advanced AI systems",
        key_points=["Point 1", "Point 2"],
        sources=["Source 1", "Source 2"],
        relevance_score=0.85,
        status=ResearchStatus.PENDING
    )

    categories = curator._categorize_content(finding)

    assert len(categories) >= 1
    assert "Machine Learning" in categories or "Natural Language Processing" in categories
