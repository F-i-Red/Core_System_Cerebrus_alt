"""
Justice Module
--------------

This module implements the restorative justice pipeline of the Cerebrus Engine.
It handles incident evaluation, victim protection, aggressor containment,
restorative assemblies, and integration with mobility and housing modules.

The system prioritizes:
1. Immediate protection of the victim.
2. Restriction of aggressor access to prevent escalation.
3. Restorative processes whenever possible.
4. Containment measures with mandatory periodic review.
5. Full transparency and auditability.

This module is intentionally simplified but demonstrates how a real
restorative justice system could integrate with the Cerebrus Engine.
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any, Callable


# ---------------------------------------------------------
# Data Models
# ---------------------------------------------------------

@dataclass
class Incident:
    """Represents a justice incident reported in the system."""
    id: str
    type: str  # e.g., "violence", "harassment", "anomalous_organic_material"
    description: str
    victim_id: Optional[str] = None
    aggressor_id: Optional[str] = None
    severity: str = "medium"


@dataclass
class JusticeDecision:
    """Represents the final decision for an incident."""
    incident_id: str
    risk_level: str
    victim_protection: Dict[str, Any]
    aggressor_restrictions: Dict[str, Any]
    restorative_process: Dict[str, Any]
    containment: Dict[str, Any]


# ---------------------------------------------------------
# Justice Module
# ---------------------------------------------------------

class JusticeModule:
    """
    Core restorative justice module.

    Handles:
    - Risk evaluation
    - Victim protection
    - Aggressor access restrictions
    - Restorative assemblies
    - Containment decisions
    - Integration with mobility and housing
    """

    def __init__(self):
        pass

    # -----------------------------------------------------
    # Risk Evaluation
    # -----------------------------------------------------

    def evaluate_risk(self, incident: Incident) -> str:
        """
        Evaluates the risk level of an incident.

        Returns:
            str: "low", "medium", "high", or "critical"
        """

        if incident.type == "anomalous_organic_material":
            return "high"

        if incident.type in ["violence", "harassment"]:
            if incident.severity == "high":
                return "critical"
            return "high"

        return "medium"

    # -----------------------------------------------------
    # Victim Protection
    # -----------------------------------------------------

    def protect_victim(
        self,
        victim_id: str,
        request_vehicle_fn: Callable[[], Dict[str, Any]],
        assign_house_fn: Callable[[], Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Protects the victim by:
        - Requesting a secure transport
        - Assigning a safe temporary house

        The functions are injected from the engine to avoid circular imports.
        """

        vehicle = request_vehicle_fn()
        house = assign_house_fn()

        return {
            "transport_assigned": vehicle,
            "safe_house_assigned": house
        }

    # -----------------------------------------------------
    # Aggressor Restrictions
    # -----------------------------------------------------

    def restrict_aggressor_access(self, aggressor_id: str) -> Dict[str, Any]:
        """
        Restricts aggressor access to:
        - Shared housing
        - Mobility services
        - Sensitive areas

        This is a placeholder for a more complex access control system.
        """

        return {
            "aggressor_id": aggressor_id,
            "restrictions": [
                "mobility_services_blocked",
                "shared_housing_blocked",
                "restricted_from_sensitive_zones"
            ]
        }

    # -----------------------------------------------------
    # Restorative Assembly
    # -----------------------------------------------------

    def restorative_assembly(self, incident: Incident) -> Dict[str, Any]:
        """
        Creates a restorative assembly plan.

        In a real system, this would involve:
        - Mediators
        - Community representatives
        - Victim preferences
        - Aggressor rehabilitation requirements
        """

        return {
            "assembly_required": True,
            "focus": "restoration_and_reintegration",
            "incident_type": incident.type
        }

    # -----------------------------------------------------
    # Containment Decision
    # -----------------------------------------------------

    def containment_decision(self, risk_level: str) -> Dict[str, Any]:
        """
        Decides the containment level for the aggressor.

        Returns:
            dict: containment plan with mandatory review.
        """

        if risk_level == "critical":
            return {
                "level": "community_internment",
                "review_in_days": 7
            }

        if risk_level == "high":
            return {
                "level": "intensive_monitoring",
                "review_in_days": 14
            }

        return {
            "level": "light_monitoring",
            "review_in_days": 30
        }

    # -----------------------------------------------------
    # Full Incident Processing Pipeline
    # -----------------------------------------------------

    def process_incident(
        self,
        incident: Incident,
        request_vehicle_fn: Callable[[], Dict[str, Any]],
        assign_house_fn: Callable[[], Dict[str, Any]]
    ) -> JusticeDecision:
        """
        Full justice pipeline:

        1. Evaluate risk
        2. Protect victim
        3. Restrict aggressor access
        4. Create restorative assembly
        5. Decide containment level

        Returns:
            JusticeDecision: structured result for logging and UI.
        """

        risk = self.evaluate_risk(incident)

        victim_protection = {}
        if incident.victim_id:
            victim_protection = self.protect_victim(
                incident.victim_id,
                request_vehicle_fn,
                assign_house_fn
            )

        aggressor_restrictions = {}
        if incident.aggressor_id:
            aggressor_restrictions = self.restrict_aggressor_access(
                incident.aggressor_id
            )

        restorative = self.restorative_assembly(incident)
        containment = self.containment_decision(risk)

        return JusticeDecision(
            incident_id=incident.id,
            risk_level=risk,
            victim_protection=victim_protection,
            aggressor_restrictions=aggressor_restrictions,
            restorative_process=restorative,
            containment=containment
        )
