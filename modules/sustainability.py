"""
Sustainability Module
---------------------

This module provides long-term sustainability metrics for the Cerebrus Engine.
It integrates ecological flows, resource efficiency, emissions, and resilience
indicators into a unified sustainability score.

It also generates alerts and recommended actions, which can be forwarded to:
- Civic Force (for inspections or interventions)
- Ecology module (for flow adjustments)
- Public dashboards (for transparency)

This module acts as a high-level "umbrella" for environmental intelligence.
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional, List


# ---------------------------------------------------------
# Data Models
# ---------------------------------------------------------

@dataclass
class SustainabilityIndicator:
    """Represents a single sustainability indicator."""
    name: str
    value: float  # 0.0 to 1.0
    description: str


@dataclass
class SustainabilityAlert:
    """Represents a sustainability alert triggered by low indicators."""
    indicator: str
    level: str  # "attention", "warning", "critical"
    message: str
    value: float


# ---------------------------------------------------------
# Sustainability Module
# ---------------------------------------------------------

class SustainabilityModule:
    """
    Core sustainability module.

    Tracks:
    - Resource efficiency
    - Renewable energy ratio
    - Waste circularity
    - Water resilience
    - CO2 emissions intensity
    - Green infrastructure coverage

    Provides:
    - Sustainability score
    - Alerts
    - Recommended actions
    - Dashboard-ready data
    """

    def __init__(self):
        # Initial indicators (0.0 to 1.0)
        self.indicators: Dict[str, SustainabilityIndicator] = {
            "renewable_energy_ratio": SustainabilityIndicator(
                name="renewable_energy_ratio",
                value=0.65,
                description="Percentage of energy sourced from renewables."
            ),
            "water_resilience": SustainabilityIndicator(
                name="water_resilience",
                value=0.72,
                description="Capacity to maintain water supply under stress."
            ),
            "waste_circularity": SustainabilityIndicator(
                name="waste_circularity",
                value=0.58,
                description="Percentage of waste that is reused or recycled."
            ),
            "co2_intensity": SustainabilityIndicator(
                name="co2_intensity",
                value=0.40,
                description="Inverse measure of CO2 emissions per capita."
            ),
            "green_infrastructure": SustainabilityIndicator(
                name="green_infrastructure",
                value=0.55,
                description="Coverage of parks, trees, and green corridors."
            ),
        }

    # -----------------------------------------------------
    # Indicator Updates
    # -----------------------------------------------------

    def update_indicator(self, name: str, new_value: float) -> None:
        """
        Updates a sustainability indicator.

        new_value must be between 0.0 and 1.0.
        """

        if name not in self.indicators:
            raise ValueError(f"Unknown indicator: {name}")

        self.indicators[name].value = max(0.0, min(1.0, new_value))

    # -----------------------------------------------------
    # Sustainability Score
    # -----------------------------------------------------

    def compute_sustainability_score(self) -> float:
        """
        Computes an overall sustainability score between 0 and 1.

        All indicators contribute equally.
        """

        total = sum(ind.value for ind in self.indicators.values())
        return total / len(self.indicators)

    # -----------------------------------------------------
    # Alert Evaluation
    # -----------------------------------------------------

    def evaluate_alert(self, indicator: SustainabilityIndicator) -> Optional[SustainabilityAlert]:
        """
        Evaluates whether an indicator requires an alert.

        Thresholds:
        - < 0.30 → critical
        - < 0.45 → warning
        - < 0.60 → attention
        """

        v = indicator.value

        if v >= 0.60:
            return None

        if v < 0.30:
            return SustainabilityAlert(
                indicator=indicator.name,
                level="critical",
                message=f"Critical sustainability deficit in {indicator.name}.",
                value=v
            )

        if v < 0.45:
            return SustainabilityAlert(
                indicator=indicator.name,
                level="warning",
                message=f"Warning: low performance in {indicator.name}.",
                value=v
            )

        return SustainabilityAlert(
            indicator=indicator.name,
            level="attention",
            message=f"Attention: {indicator.name} below optimal levels.",
            value=v
        )

    def evaluate_all_alerts(self) -> List[SustainabilityAlert]:
        """Evaluates alerts for all indicators."""
        alerts = []
        for ind in self.indicators.values():
            alert = self.evaluate_alert(ind)
            if alert:
                alerts.append(alert)
        return alerts

    # -----------------------------------------------------
    # Recommended Actions
    # -----------------------------------------------------

    def recommended_actions(self, alert: SustainabilityAlert) -> List[str]:
        """
        Returns recommended actions based on the alert type.
        """

        if alert.indicator == "renewable_energy_ratio":
            return [
                "Increase solar panel deployment.",
                "Optimize energy storage systems.",
                "Reduce fossil-based peak loads."
            ]

        if alert.indicator == "water_resilience":
            return [
                "Expand rainwater harvesting.",
                "Improve leak detection systems.",
                "Promote low-consumption appliances."
            ]

        if alert.indicator == "waste_circularity":
            return [
                "Increase community recycling points.",
                "Expand composting programs.",
                "Improve residue sorting accuracy."
            ]

        if alert.indicator == "co2_intensity":
            return [
                "Promote electric mobility.",
                "Expand green public transport.",
                "Increase tree planting initiatives."
            ]

        if alert.indicator == "green_infrastructure":
            return [
                "Create micro-parks in dense areas.",
                "Expand tree canopy coverage.",
                "Develop green corridors between blocks."
            ]

        return ["General sustainability improvement required."]

    # -----------------------------------------------------
    # Civic Force Integration
    # -----------------------------------------------------

    def create_civic_task_from_alert(self, alert: SustainabilityAlert) -> Dict[str, Any]:
        """
        Converts a sustainability alert into a civic inspection task.
        """

        return {
            "task_type": "sustainability_inspection",
            "priority": 3 if alert.level == "critical" else 2,
            "required_skills": ["ecology", "inspection"],
            "location": "Block A",
            "alert": {
                "indicator": alert.indicator,
                "level": alert.level,
                "value": alert.value
            }
        }

    # -----------------------------------------------------
    # Dashboard Output
    # -----------------------------------------------------

    def sustainability_to_panel(self) -> Dict[str, Dict[str, Any]]:
        """
        Returns dashboard-ready sustainability data.
        """

        return {
            name: {
                "value": ind.value,
                "description": ind.description
            }
            for name, ind in self.indicators.items()
        }
