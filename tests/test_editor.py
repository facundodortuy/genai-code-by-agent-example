"""Unit tests for the Editor Agent."""
import pytest

from src.agents.editor import EditorAgent
from src.models import CuratedContent, ResearchStatus


@pytest.mark.asyncio
async def test_editor_initialization():
    """Test that Editor agent initializes correctly."""
    editor = EditorAgent(approval_threshold=0.7)
    assert editor.name == "Editor"
    assert editor.role == "Editorial Decision Maker"
    assert editor.approval_threshold == 0.7
    assert editor.agent_id is not None


@pytest.mark.asyncio
async def test_editor_approves_high_quality():
    """Test editor approves high-quality content."""
    editor = EditorAgent(approval_threshold=0.7)

    curated = CuratedContent(
        id="curated-1",
        finding_id="finding-1",
        organized_summary="# Title\n\n## Overview\nDetailed summary" + "X" * 500,
        categorization=["Machine Learning", "Deep Learning", "Neural Architectures"],
        quality_score=0.9,
        recommendations="High-quality research suitable for publication",
        status=ResearchStatus.CURATED
    )

    decision = await editor.process(curated)

    assert decision.content_id == "curated-1"
    assert decision.decision == "approved"
    assert decision.final_score >= 0.7
    assert len(decision.improvements_needed) == 0


@pytest.mark.asyncio
async def test_editor_rejects_low_quality():
    """Test editor rejects low-quality content."""
    editor = EditorAgent(approval_threshold=0.7)

    curated = CuratedContent(
        id="curated-2",
        finding_id="finding-2",
        organized_summary="# Title\n\nBrief summary",
        categorization=["General AI Research"],
        quality_score=0.5,
        recommendations="Needs significant improvement before publication",
        status=ResearchStatus.CURATED
    )

    decision = await editor.process(curated)

    assert decision.content_id == "curated-2"
    assert decision.decision == "rejected"
    assert decision.final_score < 0.7
    assert len(decision.improvements_needed) > 0


@pytest.mark.asyncio
async def test_editor_custom_threshold():
    """Test editor with custom approval threshold."""
    editor = EditorAgent(approval_threshold=0.8)

    curated = CuratedContent(
        id="curated-3",
        finding_id="finding-3",
        organized_summary="# Title\n\n## Overview\nGood summary" + "X" * 400,
        categorization=["NLP", "Machine Learning"],
        quality_score=0.75,
        recommendations="Good research quality, minor improvements recommended",
        status=ResearchStatus.CURATED
    )

    decision = await editor.process(curated)

    # With higher threshold, this might be rejected
    assert decision.content_id == "curated-3"
    assert isinstance(decision.final_score, float)
    assert 0.0 <= decision.final_score <= 1.0
