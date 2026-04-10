# modules/justice.py

from dataclasses import dataclass
from typing import List, Dict, Optional, Literal
import random

IncidentType = Literal[
    "violencia",
    "perseguicao",
    "materia_organica_anomala",
    "acidente_grave",
    "ameaça",
]

RiskLevel = Literal["baixo", "medio", "alto", "critico"]

ContainmentStatus = Literal[
    "nenhuma",
    "monitorizacao",
    "restricao_acessos",
    "confinamento_temporario",
    "internacao_comunitaria"
]


@dataclass
class Incident:
    id: str
    type: IncidentType
    victim_id: Optional[str]
    aggressor_id: Optional[str]
    location: str
    details: str
    risk: RiskLevel = "baixo"
    resolved: bool = False


@dataclass
class JusticeAction:
    incident_id: str
    action: str
    details: str


@dataclass
class ContainmentDecision:
    aggressor_id: str
    level: ContainmentStatus
    reason: str
    review_in_days: int


# --------------------------
# Avaliação de risco
# --------------------------

def evaluate_risk(incident: Incident, history: List[Incident]) -> RiskLevel:
    """
    Avalia risco com base em:
    - reincidência
    - tipo de incidente
    - proximidade física
    - padrões anteriores
    """

    score = 0

    # tipo de incidente
    if incident.type == "materia_organica_anomala":
        score += 5
    if incident.type == "violencia":
        score += 4
    if incident.type == "perseguicao":
        score += 3
    if incident.type == "ameaça":
        score += 2

    # reincidência
    if incident.aggressor_id:
        past = [i for i in history if i.aggressor_id == incident.aggressor_id]
        score += len(past)

    # thresholds
    if score >= 7:
        return "critico"
    if score >= 5:
        return "alto"
    if score >= 3:
        return "medio"
    return "baixo"


# --------------------------
# Proteção imediata da vítima
# --------------------------

def protect_victim(victim_id: str) -> JusticeAction:
    """
    Atribui habitação suplente segura e acompanhamento.
    """
    return JusticeAction(
        incident_id="N/A",
        action="protecao_vitima",
        details=f"Vítima {victim_id} movida para habitação segura e atribuída equipa de apoio."
    )


# --------------------------
# Bloqueio de acessos do agressor
# --------------------------

def restrict_aggressor_access(aggressor_id: str) -> JusticeAction:
    """
    Bloqueia transportes, terminais e casas partilhadas.
    """
    return JusticeAction(
        incident_id="N/A",
        action="restricao_acessos",
        details=f"Agressor {aggressor_id} com acessos bloqueados à rede comunitária."
    )


# --------------------------
# Contenção auditada
# --------------------------

def containment_decision(incident: Incident) -> ContainmentDecision:
    """
    Decide nível de contenção com base no risco.
    """

    if incident.risk == "baixo":
        return ContainmentDecision(
            aggressor_id=incident.aggressor_id,
            level="monitorizacao",
            reason="Risco baixo",
            review_in_days=30
        )

    if incident.risk == "medio":
        return ContainmentDecision(
            aggressor_id=incident.aggressor_id,
            level="restricao_acessos",
            reason="Risco médio",
            review_in_days=30
        )

    if incident.risk == "alto":
        return ContainmentDecision(
            aggressor_id=incident.aggressor_id,
            level="confinamento_temporario",
            reason="Risco alto",
            review_in_days=15
        )

    # risco crítico
    return ContainmentDecision(
        aggressor_id=incident.aggressor_id,
        level="internacao_comunitaria",
        reason="Risco crítico — ameaça persistente",
        review_in_days=7
    )


# --------------------------
# Assembleia restaurativa
# --------------------------

def restorative_assembly(incident: Incident) -> JusticeAction:
    """
    Cria assembleia restaurativa ampliada.
    """
    return JusticeAction(
        incident_id=incident.id,
        action="assembleia_restaurativa",
        details="Assembleia convocada para discutir reparação, impacto e medidas comunitárias."
    )


# --------------------------
# Pipeline principal
# --------------------------

def process_incident(
    incident: Incident,
    history: List[Incident]
) -> List[JusticeAction]:
    """
    Pipeline completo:
    - avaliar risco
    - proteger vítima
    - restringir agressor
    - assembleia restaurativa
    - contenção auditada
    """

    actions: List[JusticeAction] = []

    # 1) avaliar risco
    incident.risk = evaluate_risk(incident, history)

    # 2) proteger vítima
    if incident.victim_id:
        actions.append(protect_victim(incident.victim_id))

    # 3) restringir agressor
    if incident.aggressor_id:
        actions.append(restrict_aggressor_access(incident.aggressor_id))

    # 4) assembleia restaurativa
    actions.append(restorative_assembly(incident))

    # 5) contenção auditada
    if incident.aggressor_id:
        decision = containment_decision(incident)
        actions.append(
            JusticeAction(
                incident_id=incident.id,
                action="contencao",
                details=f"{decision.level} — revisão em {decision.review_in_days} dias"
            )
        )

    incident.resolved = True
    return actions
