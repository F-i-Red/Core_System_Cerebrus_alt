"""
Housing Module
--------------

This module manages the allocation of houses to families within the Cerebrus Engine.
It provides simple assignment logic, returning structured results that can be logged
and displayed in the public dashboard.

The module is intentionally minimal: it acts as a placeholder for a future, more
complex housing allocation system (waiting lists, priority rules, accessibility
requirements, etc.).
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class House:
    """Represents a housing unit in the system."""
    id: str
    type: str
    location: str
    occupied: bool = False


@dataclass
class Family:
    """Represents a family requesting housing."""
    id: str
    name: str
    members: int
    priority: int = 1  # Placeholder for future priority logic


@dataclass
class HousingAssignmentResult:
    """Result of a housing assignment attempt."""
    success: bool
    house_id: Optional[str]
    family_id: Optional[str]
    message: str
    details: Dict[str, Any]


class HousingModule:
    """
    Simple housing allocation module.

    This module assigns a predefined house to a predefined family.
    It is intentionally simple and acts as a demonstration of how
    a real housing system could integrate with the Cerebrus Engine.
    """

    def __init__(self):
        # Placeholder demo data
        self.available_house = House(
            id="H-001",
            type="T2",
            location="Block A — Sector 3",
            occupied=False
        )

        self.demo_family = Family(
            id="F-001",
            name="Silva Family",
            members=3,
            priority=1
        )

    def assign_house(self) -> HousingAssignmentResult:
        """
        Assigns the demo house to the demo family.

        Returns:
            HousingAssignmentResult: structured result for logging and UI display.
        """

        if self.available_house.occupied:
            return HousingAssignmentResult(
                success=False,
                house_id=self.available_house.id,
                family_id=self.demo_family.id,
                message="House is already occupied.",
                details={
                    "house_type": self.available_house.type,
                    "location": self.available_house.location,
                    "family": self.demo_family.name
                }
            )

        # Perform assignment
        self.available_house.occupied = True

        return HousingAssignmentResult(
            success=True,
            house_id=self.available_house.id,
            family_id=self.demo_family.id,
            message="House successfully assigned to family.",
            details={
                "house_type": self.available_house.type,
                "location": self.available_house.location,
                "family": self.demo_family.name,
                "members": self.demo_family.members,
                "priority": self.demo_family.priority
            }
        )
