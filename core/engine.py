# core/engine.py

from dataclasses import dataclass, field
from typing import Dict, List, Any

# Core types
from core.types import Family, House

# Updated modules (new architecture)
from modules.housing import HousingModule
from modules.mobility import MobilityModule
from modules.logistics import LogisticsModule, LogisticsRequest
from modules.civic_force import CivicForceModule
from modules.justice import JusticeModule, Incident
from modules.education import EducationModule, Vote, Institution, Specialization, CurriculumPath, TrainingProject
from modules.anti_capture import AntiCaptureModule
from modules.ecology import EcologyModule
from modules.sustainability import SustainabilityModule
from modules.tech_public_data import PublicLedger


@dataclass
class CerebrusEngine:
    """
    Central orchestrator of the Cerebrus OS.
    Manages state, coordinates modules, and logs all public actions.
    """

    # Base State
    families: Dict[str, Family] = field(default_factory=dict)
    houses: Dict[str, House] = field(default_factory=dict)
    fleet: Dict[str, Any] = field(default_factory=dict)
    civic_members: Dict[str, Any] = field(default_factory=dict)
    logistics_requests: Dict[str, LogisticsRequest] = field(default_factory=dict)
    incidents: Dict[str, Incident] = field(default_factory=dict)
    institutions: Dict[str, Institution] = field(default_factory=dict)
    specializations: Dict[str, Specialization] = field(default_factory=dict)
    curriculum_paths: Dict[str, CurriculumPath] = field(default_factory=dict)
    training_projects: Dict[str, TrainingProject] = field(default_factory=dict)

    # Transparency
    ledger: PublicLedger = field(default_factory=PublicLedger)

    # Modules
    housing: HousingModule = field(default_factory=HousingModule)
    mobility: MobilityModule = field(default_factory=MobilityModule)
    logistics: LogisticsModule = field(default_factory=LogisticsModule)
    justice: JusticeModule = field(default_factory=JusticeModule)
    civic_force: CivicForceModule = field(default_factory=CivicForceModule)
    education: EducationModule = field(default_factory=EducationModule)
    anti_capture: AntiCaptureModule = field(default_factory=AntiCaptureModule)
    ecology: EcologyModule = field(default_factory=EcologyModule)
    sustainability: SustainabilityModule = field(default_factory=SustainabilityModule)

    # ---------------------------------------------------------
    # Housing
    # ---------------------------------------------------------

    def request_house(self):
        """
        Assigns the demo house to the demo family (simple demo logic).
        """
        result = self.housing.assign_house()

        self.ledger.append(
            module="housing",
            action="house_assignment",
            details=result.details,
            visibility="public"
        )

        return result

    # ---------------------------------------------------------
    # Mobility
    # ---------------------------------------------------------

    def request_transport(self):
        """
        Assigns a vehicle to a demo transport request.
        """
        result = self.mobility.assign_transport()

        self.ledger.append(
            module="mobility",
            action="transport_assignment",
            details=result.details,
            visibility="public"
        )

        return result

    # ---------------------------------------------------------
    # Logistics
    # ---------------------------------------------------------

    def send_residue(self, content: str = "mixed residue"):
        """
        Processes a residue request and triggers justice if anomaly detected.
        """
        req = LogisticsRequest(
            id="LOG-001",
            type="residue",
            origin="Block A",
            content=content
        )

        scan = self.logistics.process_residue_request(req)

        self.ledger.append(
            module="logistics",
            action="residue_scan",
            details={
                "fraction": scan.fraction,
                "purity": scan.purity,
                "destination": scan.destination,
                "alert": scan.alert
            },
            visibility="public"
        )

        # Bridge to justice
        if scan.alert == "anomalous_organic_material":
            incident = Incident(
                id="INC-001",
                type="anomalous_organic_material",
                description="Detected biological anomaly in residue flow."
            )
            self.incidents[incident.id] = incident

            self.ledger.append(
                module="justice",
                action="incident_created",
                details={"incident_id": incident.id},
                visibility="public"
            )

        return scan

    # ---------------------------------------------------------
    # Justice
    # ---------------------------------------------------------

    def process_incident(self, incident_id: str = "INC-001"):
        """
        Runs the full justice pipeline for an incident.
        """
        incident = self.incidents.get(incident_id)
        if not incident:
            return {"error": "Incident not found"}

        result = self.justice.process_incident(
            incident,
            request_vehicle_fn=self.mobility.assign_transport,
            assign_house_fn=self.housing.assign_house
        )

        self.ledger.append(
            module="justice",
            action="incident_processed",
            details={
                "incident_id": incident_id,
                "risk": result.risk_level,
                "containment": result.containment
            },
            visibility="public"
        )

        return result

    # ---------------------------------------------------------
    # Civic Force
    # ---------------------------------------------------------

    def civic_intervention(self, description="urgent situation", location="Block A"):
        """
        Creates an urgent task and assigns a civic force member.
        """
        result = self.civic_force.civic_force_intervention(description, location)

        self.ledger.append(
            module="civic_force",
            action="intervention",
            details={"task": result["task"].id},
            visibility="public"
        )

        return result

    # ---------------------------------------------------------
    # Ecology
    # ---------------------------------------------------------

    def update_ecology(self):
        """
        Randomly updates ecology flows and returns dashboard data.
        """
        # Demo update
        self.ecology.update_flow("water", consumed=5, regenerated=7)
        self.ecology.update_flow("energy", consumed=10, regenerated=8)
        self.ecology.update_flow("waste", consumed=3, regenerated=1)
        self.ecology.update_flow("co2", consumed=4, regenerated=2)

        panel = self.ecology.ecology_to_panel()

        self.ledger.append(
            module="ecology",
            action="update",
            details=panel,
            visibility="public"
        )

        return panel

    # ---------------------------------------------------------
    # Sustainability
    # ---------------------------------------------------------

    def sustainability_panel(self):
        """
        Returns sustainability indicators, score, and alerts.
        """
        panel = self.sustainability.sustainability_to_panel()
        score = self.sustainability.compute_sustainability_score()
        alerts = self.sustainability.evaluate_all_alerts()

        self.ledger.append(
            module="sustainability",
            action="panel_requested",
            details={"score": score},
            visibility="public"
        )

        return {
            "score": score,
            "indicators": panel,
            "alerts": [
                {
                    "indicator": a.indicator,
                    "level": a.level,
                    "value": a.value,
                    "message": a.message
                }
                for a in alerts
            ]
        }

    def sustainability_actions(self):
        """
        Returns recommended actions for all sustainability alerts.
        """
        alerts = self.sustainability.evaluate_all_alerts()

        actions = {
            alert.indicator: self.sustainability.recommended_actions(alert)
            for alert in alerts
        }

        self.ledger.append(
            module="sustainability",
            action="actions_requested",
            details={"alerts": list(actions.keys())},
            visibility="public"
        )

        return actions

    def sustainability_to_civic_tasks(self):
        """
        Converts sustainability alerts into civic force tasks.
        """
        alerts = self.sustainability.evaluate_all_alerts()
        tasks = []

        for alert in alerts:
            task_data = self.sustainability.create_civic_task_from_alert(alert)
            task = self.civic_force.create_task(
                task_type=task_data["task_type"],
                priority=task_data["priority"],
                required_skills=task_data["required_skills"],
                location=task_data["location"]
            )
            tasks.append(task.id)

        self.ledger.append(
            module="sustainability",
            action="tasks_created",
            details={"tasks": tasks},
            visibility="public"
        )

        return {"created_tasks": tasks}

    # ---------------------------------------------------------
    # Public Logs
    # ---------------------------------------------------------

    def get_logs(self):
        """Returns all public ledger entries."""
        return self.ledger.get_public()
