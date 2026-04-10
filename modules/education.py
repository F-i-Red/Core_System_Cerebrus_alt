# modules/education.py

from dataclasses import dataclass
from typing import List, Dict, Optional, Literal

InstitutionType = Literal["escola", "universidade", "centro_formacao"]

ProposalStatus = Literal["aberta", "fechada"]


@dataclass
class Institution:
    id: str
    name: str
    type: InstitutionType
    location: str
    members: List[str]  # lista de person_id


@dataclass
class Specialization:
    person_id: str
    tags: List[str]  # ex: ["saude", "educacao", "engenharia"]


@dataclass
class Proposal:
    id: str
    title: str
    description: str
    context: str          # ex: "saude", "educacao", "mobilidade"
    status: ProposalStatus = "aberta"


@dataclass
class Vote:
    proposal_id: str
    person_id: str
    choice: bool          # True = a favor, False = contra


@dataclass
class TallyResult:
    proposal_id: str
    total_weight_for: float
    total_weight_against: float
    approved: bool
    reason: str


# --------------------------
# Funções internas
# --------------------------

def get_vote_weight(
    person_id: str,
    specializations: Dict[str, Specialization],
    institutions: Dict[str, Institution],
    proposal: Proposal
) -> float:
    """
    Peso do voto:
    - base: 1
    - +1 se tiver especialização no contexto (ex: "saude")
    - +1 se for membro de instituição diretamente ligada (escola para educação, etc.)
    """

    weight = 1.0

    spec = specializations.get(person_id)
    if spec and proposal.context in spec.tags:
        weight += 1.0

    # se for educação e a pessoa estiver numa escola → +1
    if proposal.context == "educacao":
        for inst in institutions.values():
            if inst.type == "escola" and person_id in inst.members:
                weight += 1.0
                break

    # se for saúde e a pessoa tiver "saude" → já foi contado acima
    # podemos expandir isto depois para outros contextos

    return weight


# --------------------------
# API principal
# --------------------------

def tally_votes(
    proposal: Proposal,
    votes: List[Vote],
    specializations: Dict[str, Specialization],
    institutions: Dict[str, Institution]
) -> TallyResult:
    """
    Conta votos com peso, decide aprovação.
    Regra simples:
    - aprovado se peso_a_favor >= 1.2 * peso_contra
    """

    total_for = 0.0
    total_against = 0.0

    for v in votes:
        if v.proposal_id != proposal.id:
            continue

        w = get_vote_weight(v.person_id, specializations, institutions, proposal)

        if v.choice:
            total_for += w
        else:
            total_against += w

    if total_for == 0 and total_against == 0:
        return TallyResult(
            proposal_id=proposal.id,
            total_weight_for=0.0,
            total_weight_against=0.0,
            approved=False,
            reason="Sem votos registados"
        )

    if total_for >= 1.2 * total_against:
        proposal.status = "fechada"
        return TallyResult(
            proposal_id=proposal.id,
            total_weight_for=total_for,
            total_weight_against=total_against,
            approved=True,
            reason="Aprovado por maioria ponderada"
        )

    proposal.status = "fechada"
    return TallyResult(
        proposal_id=proposal.id,
        total_weight_for=total_for,
        total_weight_against=total_against,
        approved=False,
        reason="Rejeitado ou sem maioria suficiente"
    )
