# core/engine.py

from dataclasses import dataclass, field
from typing import Dict, List

from core.types import Family, House
from modules import housing, mobility, civic_force, logistics, education, justice, tech_public_data


@dataclass
class CerebrusEngine:
    # Estado base
    families: Dict[str, Family] = field(default_factory=dict)
    houses: Dict[str, House] = field(default_factory=dict)
    fleet: Dict[str, object] = field(default_factory=dict)
    civic_members: Dict[str, civic_force.CivicForceMember] = field(default_factory=dict)
    logistics_requests: Dict[str, logistics.LogisticsRequest] = field(default_factory=dict)
    incidents: Dict[str, justice.Incident] = field(default_factory=dict)
    institutions: Dict[str, education.Institution] = field(default_factory=dict)
    specializations: Dict[str, education.Specialization] = field(default_factory=dict)
    curriculum_paths: Dict[str, education.CurriculumPath] = field(default_factory=dict)
    training_projects: Dict[str, education.TrainingProject] = field(default_factory=dict)

    # Tecnologia & dados públicos
    ledger: tech_public_data.PublicLedger = field(default_factory=tech_public_data.PublicLedger)
    panels: Dict[str, tech_public_data.NeighborhoodPanel] = field(default_factory=dict)

    # --------------------------
    # Habitação
    # --------------------------

    def request_house(self, house_id: str, family_id: str, house_type: str):
        fam = self.families[family_id]
        house_obj = self.houses[house_id]

        req = housing.HouseRequest(
            family_id=family_id,
            house_id=house_id,
            requested_type=house_type
        )

        result = housing.allocate_house(
            house=house_obj,
            families_by_id=self.families,
            requests=[req]
        )

        if result.allocated_family_id == family_id:
            housing.assign_house(house_obj, fam, list(self.houses.values()))
            self.ledger.add_log(
                module="housing",
                action="house_allocated",
                details={"house_id": house_id, "family_id": family_id}
            )

        return result

    # --------------------------
    # Mobilidade
    # --------------------------

    def request_mobility(self, person_id: str, origin: str, destination: str, priority: int = 0):
        req = mobility.MobilityRequest(
            person_id=person_id,
            origin=origin,
            destination=destination,
            priority=priority
        )
        assignment = mobility.request_vehicle(self.fleet, req)
        self.ledger.add_log(
            module="mobility",
            action="request_vehicle",
            details={"person_id": person_id, "origin": origin, "destination": destination, "result": assignment.reason}
        )
        return assignment

    # --------------------------
    # Logística
    # --------------------------

    def submit_logistics_request(self, req_id: str, person_id: str, req_type: str, content: str, location: str):
        req = logistics.LogisticsRequest(
            id=req_id,
            person_id=person_id,
            type=req_type,  # "encomenda" ou "residuo"
            content=content,
            location=location
        )
        self.logistics_requests[req_id] = req
        result = logistics.process_logistics_request(self.fleet, req)

        # se for resíduo com alerta → criar incidente
        if isinstance(result, logistics.ResidueScanResult) and result.alert == "materia_organica_anomala":
            incident_id = f"incident_{req_id}"
            inc = justice.Incident(
                id=incident_id,
                type="materia_organica_anomala",
                victim_id=None,
                aggressor_id=None,
                location=result.destination,
                details="Deteção de matéria orgânica anómala no fluxo de resíduos."
            )
            self.incidents[incident_id] = inc
            self.ledger.add_log(
                module="justice",
                action="incident_created",
                details={"incident_id": incident_id, "type": inc.type}
            )

        return result

    # --------------------------
    # Justiça
    # --------------------------

    def process_incident(self, incident_id: str):
        incident = self.incidents[incident_id]
        history = [i for i in self.incidents.values() if i.id != incident_id]

        actions = justice.process_incident(incident, history)

        for act in actions:
            self.ledger.add_log(
                module="justice",
                action=act.action,
                details={"incident_id": incident_id, "details": act.details}
            )

        return actions

    # --------------------------
    # Força Cívica
    # --------------------------

    def dispatch_civic_force(self, incident_id: str):
        incident = self.incidents[incident_id]
        msg = civic_force.civic_force_intervention(self.civic_members, incident)
        self.ledger.add_log(
            module="civic_force",
            action="intervention",
            details={"incident_id": incident_id, "message": msg}
        )
        return msg

    # --------------------------
    # Educação
    # --------------------------

    def tally_proposal_votes(self, proposal: education.Proposal, votes: List[education.Vote]):
        result = education.tally_votes(
            proposal=proposal,
            votes=votes,
            specializations=self.specializations,
            institutions=self.institutions
        )
        self.ledger.add_log(
            module="education",
            action="tally_votes",
            details={
                "proposal_id": proposal.id,
                "approved": result.approved,
                "for": result.total_weight_for,
                "against": result.total_weight_against
            }
        )
        return result

    # --------------------------
    # Painéis de bairro
    # --------------------------

    def update_panel(self, panel_id: str, data: dict):
        panel = self.panels.get(panel_id)
        if not panel:
            panel = tech_public_data.NeighborhoodPanel(id=panel_id, public_data={})
            self.panels[panel_id] = panel
        panel.update(data)
        self.ledger.add_log(
            module="tech_public_data",
            action="panel_update",
            details={"panel_id": panel_id, "keys": list(data.keys())}
        )
        return panel
