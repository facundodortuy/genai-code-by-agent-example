"""Data models for the AI research system."""
from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class ResearchStatus(str, Enum):
    """Status of research content."""
    PENDING = "pending"
    CURATED = "curated"
    APPROVED = "approved"
    REJECTED = "rejected"


class ResearchTopic(BaseModel):
    """A research topic to investigate."""
    id: str
    topic: str
    keywords: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)


class ResearchFinding(BaseModel):
    """A research finding from the Researcher agent."""
    id: str
    topic_id: str
    title: str
    summary: str
    key_points: List[str] = Field(default_factory=list)
    sources: List[str] = Field(default_factory=list)
    relevance_score: float = Field(ge=0.0, le=1.0)
    created_at: datetime = Field(default_factory=datetime.now)
    status: ResearchStatus = ResearchStatus.PENDING


class CuratedContent(BaseModel):
    """Curated content from the Curator agent."""
    id: str
    finding_id: str
    organized_summary: str
    categorization: List[str] = Field(default_factory=list)
    quality_score: float = Field(ge=0.0, le=1.0)
    recommendations: str
    created_at: datetime = Field(default_factory=datetime.now)
    status: ResearchStatus = ResearchStatus.CURATED


class EditorialDecision(BaseModel):
    """Editorial decision from the Editor agent."""
    id: str
    content_id: str
    decision: str  # "approved" or "rejected"
    reasoning: str
    improvements_needed: List[str] = Field(default_factory=list)
    final_score: float = Field(ge=0.0, le=1.0)
    created_at: datetime = Field(default_factory=datetime.now)


class ResearchReport(BaseModel):
    """Complete research report combining all stages."""
    topic: ResearchTopic
    finding: ResearchFinding
    curated: Optional[CuratedContent] = None
    decision: Optional[EditorialDecision] = None
    final_status: ResearchStatus
    created_at: datetime = Field(default_factory=datetime.now)
