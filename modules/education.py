"""
Education Module
----------------

This module defines the educational and institutional structures used by
the Cerebrus Engine. It provides:

- Weighted voting based on specialization and institutional role
- Curriculum paths for training and rehabilitation
- Training projects assigned to individuals
- Integration with restorative justice processes

The philosophy:
People with relevant expertise have proportionally more influence on
decisions in their domain, while still preserving democratic balance.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


# ---------------------------------------------------------
# Data Models
# ---------------------------------------------------------

@dataclass
class Institution:
    """Represents an institution in the community (e.g., school, clinic, lab)."""
    id: str
    name: str
    domain: str  # e.g., "education", "health", "engineering", "justice"


@dataclass
class Specialization:
    """Represents a person's area of expertise."""
    id: str
    name: str
    domain: str  # e.g., "ecology", "mobility", "logistics", "justice"


@dataclass
class CurriculumPath:
    """
    Represents a structured learning path.

    Tags allow matching with:
    - rehabilitation needs
    - institutional roles
    - community development goals
    """
    id: str
    name: str
    tags: List[str]
    modules: List[str]


@dataclass
class TrainingProject:
    """Represents a training project assigned to a person."""
    id: str
    curriculum_id: str
    participants: List[str] = field(default_factory=list)
    completed: bool = False


@dataclass
class Vote:
    """Represents a single vote in a community decision."""
    voter_id: str
    choice: str  # "for" or "against"
    specialization: Optional[Specialization] = None
    institution: Optional[Institution] = None


@dataclass
class VoteResult:
    """Represents the final result of a weighted vote."""
    approved: bool
    total_for: float
    total_against: float
    reason: str


# ---------------------------------------------------------
# Education Module
# ---------------------------------------------------------

class EducationModule:
    """
    Core education module.

    Handles:
    - Weighted voting
    - Curriculum enrollment
    - Rehabilitation training assignment
    """

    def __init__(self):
        # Demo curriculum paths
        self.curricula: List[CurriculumPath] = [
            CurriculumPath(
                id="CUR-001",
                name="Restorative Practices",
                tags=["restorative", "justice"],
                modules=["mediation", "conflict_resolution", "community_dialogue"]
            ),
            CurriculumPath(
                id="CUR-002",
                name="Ecology Stewardship",
                tags=["ecology", "sustainability"],
                modules=["resource_management", "soil_health", "water_cycles"]
            )
        ]

        self.training_projects: List[TrainingProject] = []

    # -----------------------------------------------------
    # Weighted Voting
    # -----------------------------------------------------

    def get_vote_weight(
        self,
        specialization: Optional[Specialization],
        institution: Optional[Institution],
        proposal_domain: str
    ) -> float:
        """
        Computes the weight of a vote.

        Rules:
        - Base weight = 1.0
        - +0.5 if specialization matches proposal domain
        - +0.3 if institution domain matches proposal domain
        """

        weight = 1.0

        if specialization and specialization.domain == proposal_domain:
            weight += 0.5

        if institution and institution.domain == proposal_domain:
            weight += 0.3

        return weight

    def tally_votes(self, votes: List[Vote], proposal_domain: str) -> VoteResult:
        """
        Tallies weighted votes and determines approval.

        Approval rule:
        - Proposal passes if total_for >= 1.2 * total_against
        """

        total_for = 0.0
        total_against = 0.0

        for vote in votes:
            weight = self.get_vote_weight(
                vote.specialization,
                vote.institution,
                proposal_domain
            )

            if vote.choice == "for":
                total_for += weight
            else:
                total_against += weight

        approved = total_for >= 1.2 * total_against

        reason = (
            "Approved by weighted majority."
            if approved else
            "Rejected due to insufficient weighted support."
        )

        return VoteResult(
            approved=approved,
            total_for=total_for,
            total_against=total_against,
            reason=reason
        )

    # -----------------------------------------------------
    # Curriculum Enrollment
    # -----------------------------------------------------

    def enroll_in_curriculum(self, person_tags: List[str]) -> Optional[CurriculumPath]:
        """
        Enrolls a person in a curriculum based on matching tags.

        Example:
        - A person with ["restorative", "community"] will match the
          "Restorative Practices" curriculum.
        """

        for curriculum in self.curricula:
            if any(tag in person_tags for tag in curriculum.tags):
                return curriculum

        return None

    # -----------------------------------------------------
    # Rehabilitation Training
    # -----------------------------------------------------

    def assign_rehabilitation_training(self, person_id: str) -> Optional[TrainingProject]:
        """
        Assigns a rehabilitation training project to a person.

        Matches curricula with tag "restorative".
        """

        restorative_paths = [
            c for c in self.curricula if "restorative" in c.tags
        ]

        if not restorative_paths:
            return None

        curriculum = restorative_paths[0]

        project = TrainingProject(
            id=f"TP-{len(self.training_projects) + 1}",
            curriculum_id=curriculum.id,
            participants=[person_id]
        )

        self.training_projects.append(project)
        return project
