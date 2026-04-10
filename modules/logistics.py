"""
Logistics Module
----------------

This module handles logistics operations within the Cerebrus Engine,
including delivery assignments and residue processing. It acts as a
bridge between logistics, mobility, ecology, and justice.

Residue processing may trigger alerts (e.g., anomalous organic material),
which can escalate into justice incidents. Delivery requests are routed
to the mobility system for vehicle assignment.

The module is intentionally simple and serves as a demonstration of how
a real logistics system could integrate with the Cerebrus Engine.
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any, List


# ---------------------------------------------------------
# Data Models
# ---------------------------------------------------------

@dataclass
class LogisticsRequest:
    """Represents a logistics request (delivery or residue)."""
    id: str
    type: str  # "delivery" or "residue"
    origin: str
    destination: Optional[str] = None
    content: Optional[str] = None  # For residue classification


@dataclass
class ResidueScanResult:
    """Represents the result of scanning a residue container."""
    fraction: str
    purity: float
    destination: str
    alert: Optional[str] = None  # e.g., "anomalous_organic_material"


@dataclass
class DeliveryAssignmentResult:
    """Represents the result of assigning a delivery to a vehicle."""
    success: bool
    vehicle_id: Optional[str]
    message: str
    details: Dict[str, Any]


# ---------------------------------------------------------
# Logistics Module
# ---------------------------------------------------------

class LogisticsModule:
    """
    Core logistics module.

    Handles:
    - Delivery assignment (delegated to mobility)
    - Residue classification and routing
    - Automatic escalation to justice when anomalies are detected
    """

    def __init__(self):
        # Demo vehicles (simulated mobility integration)
        self.demo_fleet = [
            {"id": "V-101", "type": "Electric Van", "available": True},
            {"id": "V-102", "type": "Cargo Pod", "available": True},
        ]

    # -----------------------------------------------------
    # Residue Processing
    # -----------------------------------------------------

    def classify_residue(self, content: str) -> str:
        """
        Classifies residue based on keywords.

        Returns:
            str: residue fraction (e.g., "organic", "plastic", "metal").
        """
        content = content.lower()

        if any(k in content for k in ["food", "vegetable", "fruit", "organic"]):
            return "organic"

        if any(k in content for k in ["plastic", "bottle", "packaging"]):
            return "plastic"

        if any(k in content for k in ["metal", "aluminum", "steel"]):
            return "metal"

        if any(k in content for k in ["glass", "jar", "bottle"]):
            return "glass"

        return "mixed"

    def compute_purity(self, content: str) -> float:
        """
        Computes a simulated purity score for the residue.

        Returns:
            float: purity between 0.0 and 1.0
        """
        content = content.lower()

        if "blood" in content or "tissue" in content:
            return 0.05  # extremely low purity → anomaly

        if "mixed" in content:
            return 0.4

        return 0.85  # default high purity

    def choose_destination(self, fraction: str, purity: float) -> str:
        """
        Chooses the appropriate processing destination.
        """
        if purity < 0.1:
            return "hazardous_materials_center"

        if fraction == "organic":
            return "local_composting_unit"

        if fraction == "plastic":
            return "advanced_recycling_center"

        if fraction == "metal":
            return "regional_reuse_foundry"

        if fraction == "glass":
            return "glass_recovery_station"

        return "mixed_recycling_center"

    def process_residue_request(self, request: LogisticsRequest) -> ResidueScanResult:
        """
        Processes a residue request and returns a scan result.

        May trigger an alert if anomalous organic material is detected.
        """

        fraction = self.classify_residue(request.content or "")
        purity = self.compute_purity(request.content or "")
        destination = self.choose_destination(fraction, purity)

        alert = None
        if purity < 0.1:
            alert = "anomalous_organic_material"

        return ResidueScanResult(
            fraction=fraction,
            purity=purity,
            destination=destination,
            alert=alert
        )

    # -----------------------------------------------------
    # Delivery Processing
    # -----------------------------------------------------

    def _find_available_vehicle(self) -> Optional[Dict[str, Any]]:
        """Returns the first available vehicle."""
        for v in self.demo_fleet:
            if v["available"]:
                return v
        return None

    def assign_delivery(self, request: LogisticsRequest) -> DeliveryAssignmentResult:
        """
        Assigns a delivery request to an available vehicle.
        """

        vehicle = self._find_available_vehicle()

        if not vehicle:
            return DeliveryAssignmentResult(
                success=False,
                vehicle_id=None,
                message="No available vehicles for delivery.",
                details={"request_id": request.id}
            )

        # Mark vehicle as in service
        vehicle["available"] = False

        return DeliveryAssignmentResult(
            success=True,
            vehicle_id=vehicle["id"],
            message="Delivery assigned to vehicle.",
            details={
                "vehicle_type": vehicle["type"],
                "origin": request.origin,
                "destination": request.destination
            }
        )

    # -----------------------------------------------------
    # Main Entry Point
    # -----------------------------------------------------

    def process_logistics_request(self, request: LogisticsRequest) -> Dict[str, Any]:
        """
        Routes the request to the appropriate handler.

        Returns:
            dict: structured result for logging and UI display.
        """

        if request.type == "residue":
            scan = self.process_residue_request(request)
            return {
                "type": "residue",
                "fraction": scan.fraction,
                "purity": scan.purity,
                "destination": scan.destination,
                "alert": scan.alert
            }

        if request.type == "delivery":
            assignment = self.assign_delivery(request)
            return {
                "type": "delivery",
                "success": assignment.success,
                "vehicle_id": assignment.vehicle_id,
                "message": assignment.message,
                "details": assignment.details
            }

        return {"error": "Unknown logistics request type."}

    # -----------------------------------------------------
    # Bridge to Justice
    # -----------------------------------------------------

    def logistics_to_justice_bridge(self, scan: ResidueScanResult) -> Optional[Dict[str, Any]]:
        """
        Converts a residue anomaly into a justice incident.

        Returns:
            dict or None: incident data if anomaly detected.
        """

        if scan.alert == "anomalous_organic_material":
            return {
                "type": "anomalous_organic_material",
                "severity": "high",
                "description": "Detected biological material inconsistent with normal residue.",
            }

        return None
