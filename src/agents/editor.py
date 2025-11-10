"""Editor agent for approving or rejecting curated content."""
from src.agents.base import BaseAgent
from src.models import CuratedContent, EditorialDecision


class EditorAgent(BaseAgent):
    """Agent responsible for editorial decisions on curated content."""

    def __init__(self, approval_threshold: float = 0.7):
        """Initialize the Editor agent.

        Args:
            approval_threshold: Minimum quality score for approval (default 0.7)
        """
        super().__init__(
            name="Editor",
            role="Editorial Decision Maker"
        )
        self.approval_threshold = approval_threshold

    async def process(self, curated: CuratedContent) -> EditorialDecision:
        """Make an editorial decision on curated content.

        Args:
            curated: Curated content to review

        Returns:
            Editorial decision
        """
        self.log(f"Reviewing curated content (ID: {curated.id[:8]}...)")

        # Make editorial decision
        decision = await self._make_decision(curated)

        self.log(f"Decision: {decision.decision.upper()} (score: {decision.final_score:.2f})")
        return decision

    async def _make_decision(self, curated: CuratedContent) -> EditorialDecision:
        """Make the editorial decision.

        Args:
            curated: Curated content to evaluate

        Returns:
            Editorial decision
        """
        # Calculate final score
        final_score = self._calculate_final_score(curated)

        # Make decision based on threshold
        if final_score >= self.approval_threshold:
            decision_text = "approved"
            reasoning = self._generate_approval_reasoning(curated, final_score)
            improvements = []
        else:
            decision_text = "rejected"
            reasoning = self._generate_rejection_reasoning(curated, final_score)
            improvements = self._suggest_improvements(curated)

        decision = EditorialDecision(
            id=self.generate_id(),
            content_id=curated.id,
            decision=decision_text,
            reasoning=reasoning,
            improvements_needed=improvements,
            final_score=final_score
        )

        return decision

    def _calculate_final_score(self, curated: CuratedContent) -> float:
        """Calculate the final editorial score.

        Args:
            curated: Curated content

        Returns:
            Final score between 0 and 1
        """
        # Weight different aspects
        base_score = curated.quality_score * 0.6

        # Bonus for good categorization
        category_bonus = min(len(curated.categorization) * 0.05, 0.15)

        # Bonus for comprehensive organized summary
        summary_length = len(curated.organized_summary)
        summary_bonus = min(summary_length / 1000 * 0.15, 0.15)

        # Penalty if recommendations indicate issues
        penalty = 0.0
        if "significant improvement" in curated.recommendations.lower():
            penalty = 0.1
        elif "minor improvements" in curated.recommendations.lower():
            penalty = 0.05

        final_score = base_score + category_bonus + summary_bonus - penalty
        return min(max(final_score, 0.0), 1.0)

    def _generate_approval_reasoning(self, curated: CuratedContent, score: float) -> str:
        """Generate reasoning for approval.

        Args:
            curated: Curated content
            score: Final score

        Returns:
            Reasoning text
        """
        reasoning_parts = [
            f"Content approved with final score of {score:.2f}.",
            f"Quality assessment: {curated.quality_score:.2f}.",
        ]

        if curated.categorization:
            reasoning_parts.append(
                f"Well-categorized across {len(curated.categorization)} areas: "
                f"{', '.join(curated.categorization[:3])}."
            )

        if score >= 0.9:
            reasoning_parts.append("Exceptional quality suitable for featured publication.")
        elif score >= 0.8:
            reasoning_parts.append("High quality suitable for immediate publication.")
        else:
            reasoning_parts.append("Meets publication standards.")

        return " ".join(reasoning_parts)

    def _generate_rejection_reasoning(self, curated: CuratedContent, score: float) -> str:
        """Generate reasoning for rejection.

        Args:
            curated: Curated content
            score: Final score

        Returns:
            Reasoning text
        """
        reasoning_parts = [
            f"Content rejected with final score of {score:.2f} "
            f"(threshold: {self.approval_threshold}).",
        ]

        if curated.quality_score < 0.6:
            reasoning_parts.append("Quality score below minimum standards.")

        if len(curated.categorization) < 2:
            reasoning_parts.append("Insufficient categorization.")

        if "significant improvement" in curated.recommendations.lower():
            reasoning_parts.append("Curator identified need for major revisions.")

        reasoning_parts.append("Content requires revision before publication.")

        return " ".join(reasoning_parts)

    def _suggest_improvements(self, curated: CuratedContent) -> list:
        """Suggest improvements for rejected content.

        Args:
            curated: Curated content

        Returns:
            List of improvement suggestions
        """
        improvements = []

        if curated.quality_score < 0.6:
            improvements.append("Enhance research depth and source quality")

        if len(curated.categorization) < 2:
            improvements.append("Improve content categorization and tagging")

        if len(curated.organized_summary) < 500:
            improvements.append("Expand summary with more detailed analysis")

        if curated.quality_score < 0.7:
            improvements.append("Add more academic sources and citations")

        if "credibility" in curated.recommendations.lower():
            improvements.append("Strengthen credibility with authoritative sources")

        if not improvements:
            improvements.append("Minor quality improvements needed")

        return improvements
