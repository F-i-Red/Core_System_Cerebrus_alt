# modules/civic_force.py

from dataclasses import dataclass
from typing import List, Dict, Optional, Literal
import random

TaskType = Literal[
    "manutencao",
    "limpeza",
    "construcao",
    "inspecao",
    "estudo",
    "seguranca",
    "urgencia",
    "logistica"
]

TaskStatus = Literal[
    "pendente",
    "atribuida",
    "em_execucao",
    "concluida"
]


@dataclass
class CivicForceMember:
    id: str
    name: str
    skills: List[str]          # ex: ["eletricista", "seguranca", "saude"]
    available: bool
    location: str              # bloco / zona
    on_mission: bool = False


@dataclass
class CivicTask:
    id: str
    type: TaskType
    location: str
    priority: int              # 0 normal, 1 importante, 2 urgente, 3 crítico
    required_skills: List[str]
    status: TaskStatus = "pendente"
    assigned_member_id: Optional[str] = None
    related_vehicle_id: Optional[str] = None  # para ligar à mobilidade, se preciso


@dataclass
class TaskAssignmentResult:
    task_id: str
    member_id: Optional[str]
    reason: str


# --------------------------
# Funções internas
# --------------------------

def member_matches_task(member: CivicForceMember, task: CivicTask) -> bool:
    if not member.available or member.on_mission:
        return False
    # skills mínimas
    if task.required_skills:
        if not any(skill in member.skills for skill in task.required_skills):
            return False
    return True


def score_member_for_task(member: CivicForceMember, task: CivicTask) -> int:
    """
    Score simples:
    +10 se tiver skill necessária
    +5 se estiver no mesmo local
    + prioridade da tarefa
    """
    score = 0
    if any(skill in member.skills for skill in task.required_skills):
        score += 10
    if member.location == task.location:
        score += 5
    score += task.priority
    return score


# --------------------------
# API principal
# --------------------------

def assign_tasks(
    members: Dict[str, CivicForceMember],
    tasks: Dict[str, CivicTask],
) -> List[TaskAssignmentResult]:
    """
    Percorre tarefas pendentes e tenta atribuí-las
    a membros da Força Cívica.
    """
    results: List[TaskAssignmentResult] = []

    pending_tasks = [t for t in tasks.values() if t.status == "pendente"]
    # ordenar por prioridade (maior primeiro)
    pending_tasks.sort(key=lambda t: t.priority, reverse=True)

    for task in pending_tasks:
        # encontrar candidatos
        candidates = [
            m for m in members.values()
            if member_matches_task(m, task)
        ]

        if not candidates:
            results.append(TaskAssignmentResult(
                task_id=task.id,
                member_id=None,
                reason="Nenhum membro disponível/adequado"
            ))
            continue

        # escolher melhor candidato
        scored = [(score_member_for_task(m, task), m) for m in candidates]
        scored.sort(key=lambda x: x[0], reverse=True)
        best_score, best_member = scored[0]

        task.assigned_member_id = best_member.id
        task.status = "atribuida"
        best_member.on_mission = True

        results.append(TaskAssignmentResult(
            task_id=task.id,
            member_id=best_member.id,
            reason=f"Tarefa atribuída a {best_member.name} (score {best_score})"
        ))

    return results


def complete_task(
    members: Dict[str, CivicForceMember],
    tasks: Dict[str, CivicTask],
    task_id: str
) -> str:
    if task_id not in tasks:
        return "Tarefa inexistente"

    task = tasks[task_id]
    if task.assigned_member_id is None:
        return "Tarefa não estava atribuída"

    task.status = "concluida"
    member = members.get(task.assigned_member_id)
    if member:
        member.on_mission = False
        member.available = True

    return f"Tarefa {task_id} concluída por {task.assigned_member_id}"


def create_urgent_task(
    tasks: Dict[str, CivicTask],
    task_id: str,
    location: str,
    task_type: TaskType,
    required_skills: List[str]
) -> CivicTask:
    """
    Cria uma tarefa urgente (ex: avaria grave, inundação, acidente).
    """
    task = CivicTask(
        id=task_id,
        type=task_type,
        location=location,
        priority=3,
        required_skills=required_skills,
        status="pendente"
    )
    tasks[task_id] = task
    return task
