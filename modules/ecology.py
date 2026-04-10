"""
Ecology Module
--------------

This module tracks ecological resource flows within a neighborhood block.
It monitors consumption, regeneration, and overall ecological balance,
producing alerts when negative trends appear.

The module integrates with:
- Civic Force (for ecological inspections)
- Public dashboards (for transparency)
- Future sustainability modules

This is a simplified but functional ecological engine.
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional


# ---------------------------------------------------------
# Data Models
# ---------------------------------------------------------

@dataclass
class ResourceFlow:
    """Represents the consumption and regeneration of a resource."""
    consumed: float = 0.0
    regenerated: float = 0.0

    def balance(self) -> float:
        """Returns the net ecological balance."""
        return self.regenerated - self.consumed


@dataclass
class EcoAlert:
    """Represents an ecological alert triggered by negative balance."""
    resource: str
    level: str  # "attention", "warning", "critical"
    message: str
    balance: float


# ---------------------------------------------------------
# Ecology Module
# ---------------------------------------------------------

class EcologyModule:
    """
    Core ecology module.

    Tracks:
    - Water
    - Energy
    - Waste
    - CO2

    Provides:
    - Flow updates
    - Health score
    - Alert generation
    - Dashboard-ready data
    """

    def __init__(self):
        # Initial resource flows for Block A
        self.resources: Dict[str, ResourceFlow] = {
            "water": ResourceFlow(),
            "energy": ResourceFlow(),
            "waste": ResourceFlow(),
            "co2": ResourceFlow()
        }

    # -----------------------------------------------------
    # Flow Updates
    # -----------------------------------------------------

    def update_flow(self, resource: str, consumed: float, regenerated: float) -> None:
        """
        Updates the flow of a specific resource.
        """

        if resource not in self.resources:
            raise ValueError(f"Unknown resource: {resource}")

        self.resources[resource].consumed += consumed
        self.resources[resource].regenerated += regenerated

    # -----------------------------------------------------
    # Health Score
    # -----------------------------------------------------

    def compute_health(self) -> float:
        """
        Computes an overall ecological health score between 0 and 1.

        Formula:
        - Each resource contributes equally.
        - Positive balance increases score.
        - Negative balance decreases score.
        """

        total = 0
        count = len(self.resources)

        for flow in self.resources.values():
            bal = flow.balance()

            if bal >= 0:
                total += 1.0
            else:
                total += max(0.0, 1.0 + bal / 100.0)

        return total / count

    # -----------------------------------------------------
    # Alert Evaluation
    # -----------------------------------------------------

    def evaluate_alert(self, resource: str) -> Optional[EcoAlert]:
        """
        Evaluates whether a resource requires an ecological alert.

        Thresholds:
        - balance < 0 → attention
        - balance < -20 → warning
        - balance < -50 → critical
        """

        flow = self.resources[resource]
        bal = flow.balance()

        if bal >= 0:
            return None

        if bal < -50:
            return EcoAlert(
                resource=resource,
                level="critical",
                message=f"Critical deficit detected in {resource}.",
                balance=bal
            )

        if bal < -20:
            return EcoAlert(
                resource=resource,
                level="warning",
                message=f"Warning: significant deficit in {resource}.",
                balance=bal
            )

        return EcoAlert(
            resource=resource,
            level="attention",
            message=f"Attention: negative balance in {resource}.",
            balance=bal
        )

    # -----------------------------------------------------
    # Civic Force Integration
    # -----------------------------------------------------

    def create_civic_task_from_alert(self, alert: EcoAlert) -> Dict[str, Any]:
        """
        Converts an ecological alert into a civic inspection task.
        """

        return {
            "task_type": "ecology_inspection",
            "priority": 2 if alert.level == "attention" else 3,
            "required_skills": ["ecology", "inspection"],
            "location": "Block A",
            "alert": {
                "resource": alert.resource,
                "level": alert.level,
                "balance": alert.balance
            }
        }

    # -----------------------------------------------------
    # Dashboard Output
    # -----------------------------------------------------

    def ecology_to_panel(self) -> Dict[str, Dict[str, float]]:
        """
        Returns a dashboard-ready dictionary of resource flows.
        """

        return {
            resource: {
                "consumed": flow.consumed,
                "regenerated": flow.regenerated,
                "balance": flow.balance()
            }
            for resource, flow in self.resources.items()
        }
