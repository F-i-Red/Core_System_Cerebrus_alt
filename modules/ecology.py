# modules/ecology.py

from dataclasses import dataclass
from typing import Dict, Optional, Literal
import time
import random

ResourceType = Literal["agua", "energia", "residuos", "co2"]

AlertLevel = Literal["normal", "atencao", "alerta", "critico"]


# --------------------------
# Estruturas base
# --------------------------

@dataclass
class ResourceFlow:
    type: ResourceType
    consumed: float = 0.0
    regenerated: float = 0.0
    balance: float = 0.0
    last_update: float = 0.0


@dataclass
class EcoBlock:
    id: str
    name: str
    flows: Dict[ResourceType, ResourceFlow]
    health_score: float = 1.0  # 1.0 = perfeito, 0.0 = colapso


@dataclass
class EcoAlert:
    block_id: str
    resource: ResourceType
    level: AlertLevel
    message: str
    timestamp: float


# --------------------------
# Atualização de fluxos
# --------------------------

def update_flow(block: EcoBlock, resource: ResourceType, consumed: float, regenerated: float):
    flow = block.flows[resource]
    flow.consumed += consumed
    flow.regenerated += regenerated
    flow.balance = flow.regenerated - flow.consumed
    flow.last_update = time.time()

    # atualizar saúde ecológica
    block.health_score = compute_health(block)


# --------------------------
# Saúde ecológica
# --------------------------

def compute_health(block: EcoBlock) -> float:
    """
    Saúde ecológica baseada em:
    - balanço de água
    - balanço de energia
    - resíduos regenerados
    - emissões de CO2
    """

    agua = block.flows["agua"].balance
    energia = block.flows["energia"].balance
    residuos = block.flows["residuos"].balance
    co2 = block.flows["co2"].balance

    score = 1.0

    # água
    if agua < 0:
        score -= 0.2

    # energia
    if energia < 0:
        score -= 0.2

    # resíduos
    if residuos < 0:
        score -= 0.2

    # CO2
    if co2 > 0:
        score -= 0.2

    return max(0.0, min(1.0, score))


# --------------------------
# Alertas ecológicos
# --------------------------

def evaluate_alert(block: EcoBlock, resource: ResourceType) -> Optional[EcoAlert]:
    flow = block.flows[resource]

    if flow.balance >= 0:
        return None

    deficit = abs(flow.balance)

    if deficit < 10:
        level = "atencao"
    elif deficit < 30:
        level = "alerta"
    else:
        level = "critico"

    return EcoAlert(
        block_id=block.id,
        resource=resource,
        level=level,
        message=f"Défice de {resource}: {deficit:.1f} unidades",
        timestamp=time.time()
    )


# --------------------------
# Integração com Força Cívica
# --------------------------

def create_civic_task_from_alert(alert: EcoAlert):
    """
    Converte alerta ecológico em tarefa da Força Cívica.
    """
    from modules.civic_force import CivicTask

    task = CivicTask(
        id=f"eco_{alert.block_id}_{alert.resource}",
        type="inspecao",
        location=alert.block_id,
        priority=2 if alert.level == "alerta" else 3,
        required_skills=["ecologia", "manutencao"]
    )
    return task


# --------------------------
# Integração com Painéis Públicos
# --------------------------

def ecology_to_panel(block: EcoBlock):
    """
    Dados ecológicos para o painel do bairro.
    """
    return {
        "agua_balance": block.flows["agua"].balance,
        "energia_balance": block.flows["energia"].balance,
        "residuos_balance": block.flows["residuos"].balance,
        "co2_balance": block.flows["co2"].balance,
        "eco_health": block.health_score
    }
