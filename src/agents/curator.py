"""Curator agent for organizing and filtering research findings."""
from src.agents.base import BaseAgent
from src.models import CuratedContent, ResearchFinding, ResearchStatus


class CuratorAgent(BaseAgent):
    """Agent responsible for curating and organizing research findings."""

    def __init__(self):
        super().__init__(
            name="Curator",
            role="Research Content Curator"
        )

    async def process(self, finding: ResearchFinding) -> CuratedContent:
        """Curate a research finding.

        Args:
            finding: Research finding to curate

        Returns:
            Curated content
        """
        self.log(f"Curating research finding: {finding.title}")

        # Analyze and organize the research finding
        curated = await self._curate_content(finding)

        self.log(f"Curation complete. Quality score: {curated.quality_score:.2f}")
        return curated

    async def _curate_content(self, finding: ResearchFinding) -> CuratedContent:
        """Perform curation on the research finding.

        Args:
            finding: Research finding to curate

        Returns:
            Curated content
        """
        # Evaluate quality and organize content
        quality_score = self._assess_quality(finding)
        categories = self._categorize_content(finding)
        organized_summary = self._organize_summary(finding)
        recommendations = self._generate_recommendations(finding, quality_score)

        curated = CuratedContent(
            id=self.generate_id(),
            finding_id=finding.id,
            organized_summary=organized_summary,
            categorization=categories,
            quality_score=quality_score,
            recommendations=recommendations,
            status=ResearchStatus.CURATED
        )

        return curated

    def _assess_quality(self, finding: ResearchFinding) -> float:
        """Assess the quality of research finding.

        Args:
            finding: Research finding to assess

        Returns:
            Quality score between 0 and 1
        """
        # Quality based on multiple factors
        score = 0.0

        # Base score from relevance
        score += finding.relevance_score * 0.4

        # Points for number of sources (max 0.2)
        source_points = min(len(finding.sources) * 0.05, 0.2)
        score += source_points

        # Points for key points (max 0.2)
        key_points_count = min(len(finding.key_points) * 0.05, 0.2)
        score += key_points_count

        # Points for summary quality (length and detail)
        summary_points = min(len(finding.summary) / 500 * 0.2, 0.2)
        score += summary_points

        return min(score, 1.0)

    def _categorize_content(self, finding: ResearchFinding) -> list:
        """Categorize the research content.

        Args:
            finding: Research finding to categorize

        Returns:
            List of categories
        """
        categories = []

        title_lower = finding.title.lower()
        summary_lower = finding.summary.lower()
        combined = title_lower + " " + summary_lower

        # Categorize based on content
        ml_terms = ["machine learning", "deep learning", "neural network"]
        if any(term in combined for term in ml_terms):
            categories.append("Machine Learning")

        if any(term in combined for term in ["nlp", "natural language", "language model", "llm"]):
            categories.append("Natural Language Processing")

        if any(term in combined for term in ["computer vision", "image", "visual"]):
            categories.append("Computer Vision")

        if any(term in combined for term in ["ethics", "fairness", "bias", "responsible"]):
            categories.append("AI Ethics")

        if any(term in combined for term in ["reinforcement learning", "robotics", "agent"]):
            categories.append("Reinforcement Learning")

        if any(term in combined for term in ["transformer", "attention", "architecture"]):
            categories.append("Neural Architectures")

        if any(term in combined for term in ["application", "deployment", "real-world"]):
            categories.append("Applied AI")

        if any(term in combined for term in ["theory", "theoretical", "foundation"]):
            categories.append("Theoretical AI")

        # Add general category if none found
        if not categories:
            categories.append("General AI Research")

        return categories

    def _organize_summary(self, finding: ResearchFinding) -> str:
        """Organize and enhance the summary.

        Args:
            finding: Research finding

        Returns:
            Organized summary
        """
        # Create a well-structured summary
        organized = f"# {finding.title}\n\n"
        organized += f"## Overview\n{finding.summary}\n\n"

        if finding.key_points:
            organized += "## Key Findings\n"
            for i, point in enumerate(finding.key_points, 1):
                organized += f"{i}. {point}\n"
            organized += "\n"

        if finding.sources:
            organized += "## Academic Sources\n"
            for source in finding.sources:
                organized += f"- {source}\n"
            organized += "\n"

        organized += "## Research Metrics\n"
        organized += f"- Relevance Score: {finding.relevance_score:.2f}\n"
        organized += f"- Number of Sources: {len(finding.sources)}\n"
        organized += f"- Key Points Identified: {len(finding.key_points)}\n"

        return organized

    def _generate_recommendations(self, finding: ResearchFinding, quality_score: float) -> str:
        """Generate recommendations for the content.

        Args:
            finding: Research finding
            quality_score: Assessed quality score

        Returns:
            Recommendations text
        """
        recommendations = []

        if quality_score >= 0.8:
            recommendations.append("High-quality research suitable for publication")
        elif quality_score >= 0.6:
            recommendations.append("Good research quality, minor improvements recommended")
        else:
            recommendations.append("Needs significant improvement before publication")

        if len(finding.sources) < 3:
            recommendations.append("Consider adding more academic sources for credibility")

        if len(finding.key_points) < 3:
            recommendations.append("Expand key findings section for better clarity")

        if finding.relevance_score < 0.7:
            recommendations.append("Verify topic relevance and focus")

        if not recommendations:
            recommendations.append("Content meets all quality standards")

        return " | ".join(recommendations)
