"""
Mobility Module
---------------

This module manages the assignment of vehicles to transport requests within
the Cerebrus Engine. It provides simple fleet management logic, selecting
an available vehicle and marking it as in service.

The module is intentionally minimal and acts as a demonstration of how a
future mobility system could integrate with routing, priorities, and
real-time fleet optimization.
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any, List


@dataclass
class Vehicle:
    """Represents a vehicle in the mobility fleet."""
    id: str
    type: str
    location: str
    available: bool = True
    in_service: bool = False


@dataclass
class TransportRequest:
    """Represents a transport request made by a resident or module."""
    id: str
    origin: str
    destination: str
    priority: int = 1  # Placeholder for future priority logic


@dataclass
class TransportAssignmentResult:
    """Result of a transport assignment attempt."""
    success: bool
    vehicle_id: Optional[str]
    request_id: Optional[str]
    message: str
    details: Dict[str, Any]


class MobilityModule:
    """
    Simple mobility assignment module.

    This module assigns the first available vehicle to a predefined
    transport request. It is intentionally simple and acts as a
    demonstration of how a real mobility system could integrate with
    the Cerebrus Engine.
    """

    def __init__(self):
        # Demo fleet
        self.fleet: List[Vehicle] = [
            Vehicle(id="V-001", type="Electric Car", location="Block A"),
            Vehicle(id="V-002", type="Electric Van", location="Block B"),
            Vehicle(id="V-003", type="Autonomous Pod", location="Block C"),
        ]

        # Demo request
        self.demo_request = TransportRequest(
            id="T-001",
            origin="Block A — Sector 2",
            destination="Block C — Sector 1",
            priority=1
        )

    def _find_available_vehicle(self) -> Optional[Vehicle]:
        """Returns the first available vehicle in the fleet."""
        for v in self.fleet:
            if v.available and not v.in_service:
                return v
        return None

    def assign_transport(self) -> TransportAssignmentResult:
        """
        Assigns an available vehicle to the demo transport request.

        Returns:
            TransportAssignmentResult: structured result for logging and UI display.
        """

        vehicle = self._find_available_vehicle()

        if not vehicle:
            return TransportAssignmentResult(
                success=False,
                vehicle_id=None,
                request_id=self.demo_request.id,
                message="No available vehicles in the fleet.",
                details={
                    "origin": self.demo_request.origin,
                    "destination": self.demo_request.destination,
                    "priority": self.demo_request.priority
                }
            )

        # Perform assignment
        vehicle.available = False
        vehicle.in_service = True

        return TransportAssignmentResult(
            success=True,
            vehicle_id=vehicle.id,
            request_id=self.demo_request.id,
            message="Vehicle successfully assigned to transport request.",
            details={
                "vehicle_type": vehicle.type,
                "vehicle_location": vehicle.location,
                "origin": self.demo_request.origin,
                "destination": self.demo_request.destination,
                "priority": self.demo_request.priority
            }
        )
