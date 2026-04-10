# modules/education.py

from dataclasses import dataclass
from typing import List, Dict, Optional, Literal

InstitutionType = Literal["escola", "universidade", "centro_formacao"]
ProposalStatus = Literal["aberta", "fechada"]

# --------------------------
# Estruturas base
# --------------------------

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
class CurriculumPath:
    id: str
    name: str
    required_tags: List[str]  # ex: ["engenharia", "robotica"]
    duration_months: int
    grants_civic_force_access: bool = False  # formação obrigatória para certas tarefas


@dataclass
class TrainingProject:
    id: str
    title: str
    description: str
    institution_id: str
    curriculum_path_id: Optional[str] = None
    participants: List[str] = None

    def __post_init__(self):
        if self.participants is None:
            self.participants = []


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
# Peso de voto
# --------------------------

def get_vote_weight(
    person_id: str,
    specializations: Dict[str, Specialization],
    institutions: Dict[str, Institution],
    proposal: Proposal
) -> float:

    weight = 1.0

    # especialização no tema → +1
    spec = specializations.get(person_id)
    if spec and proposal.context in spec.tags:
        weight += 1.0

    # se for educação → escolas têm voto reforçado
    if proposal.context == "educacao":
        for inst in institutions.values():
            if inst.type == "escola" and person_id in inst.members:
                weight += 1.0
                break

    # se for saúde → profissionais de saúde têm peso
    if proposal.context == "saude":
        if spec and "saude" in spec.tags:
            weight += 1.0

    # se for mobilidade → técnicos e Força Cívica têm peso
    if proposal.context == "mobilidade":
        if spec and ("engenharia" in spec.tags or "logistica" in spec.tags):
            weight += 1.0

    return weight


# --------------------------
# Contagem de votos
# --------------------------

def tally_votes(
    proposal: Proposal,
    votes: List[Vote],
    specializations: Dict[str, Specialization],
    institutions: Dict[str, Institution]
) -> TallyResult:

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


# --------------------------
# Formação e Currículos
# --------------------------

def enroll_in_curriculum(
    person_id: str,
    curriculum: CurriculumPath,
    specializations: Dict[str, Specialization]
) -> bool:
    """
    Verifica se a pessoa tem as bases necessárias para entrar no currículo.
    Retorna True se puder entrar, False caso contrário.
    """
    spec = specializations.get(person_id)
    if not spec:
        return False

    # precisa de pelo menos uma tag base
    if not any(tag in spec.tags for tag in curriculum.required_tags):
        return False

    return True


# ligação com Justiça

def assign_rehabilitation_training(
    aggressor_id,
    curriculum_paths,
    training_projects
):
    """
    Atribui automaticamente um projeto de formação
    como parte da reparação/restauração.
    """
    for path in curriculum_paths.values():
        if "restaurativa" in path.required_tags:
            project = TrainingProject(
                id=f"rehab_{aggressor_id}",
                title="Formação Restaurativa Obrigatória",
                description="Processo de reintegração e autocontrolo.",
                institution_id="centro_formacao_geral",
                curriculum_path_id=path.id
            )
            project.participants.append(aggressor_id)
            training_projects[project.id] = project
            return project

    return None
