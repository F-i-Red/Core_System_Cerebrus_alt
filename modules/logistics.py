# modules/logistics.py

from dataclasses import dataclass
from typing import List, Dict, Optional, Literal
import random

FractionType = Literal[
    "metal",
    "plastico",
    "vidro",
    "organico",
    "misto"
]

RequestType = Literal[
    "encomenda",
    "residuo"
]

LogStatus = Literal[
    "pendente",
    "em_processamento",
    "concluido",
    "erro"
]


@dataclass
class LogisticsRequest:
    id: str
    person_id: str
    type: RequestType
    content: str
    location: str  # terminal
    status: LogStatus = "pendente"


@dataclass
class ResidueScanResult:
    request_id: str
    fraction: FractionType
    purity: float
    destination: str
    alert: Optional[str] = None


@dataclass
class DeliveryAssignment:
    request_id: str
    vehicle_id: Optional[str]
    reason: str


# --------------------------
# Funções internas
# --------------------------

def classify_residue(content: str) -> FractionType:
    """Classificação simples baseada em palavras-chave."""
    content = content.lower()
    if "metal" in content:
        return "metal"
    if "plast" in content:
        return "plastico"
    if "vidro" in content:
        return "vidro"
    if "resto" in content or "comida" in content:
        return "organico"
    return "misto"


def compute_purity() -> float:
    """Simulação de pureza (scanner real teria sensores)."""
    return round(random.uniform(0.80, 0.99), 2)


def choose_destination(fraction: FractionType) -> str:
    """Destino baseado na fração."""
    if fraction in ("metal", "plastico", "vidro"):
        return "centro_reaproveitamento_regional"
    if fraction == "organico":
        return "compostagem_local"
    return "reciclagem_avancada"


# --------------------------
# API principal
# --------------------------

def process_residue_request(
    request: LogisticsRequest
) -> ResidueScanResult:
    """Processa resíduos: classifica, mede pureza, define destino."""

    fraction = classify_residue(request.content)
    purity = compute_purity()
    destination = choose_destination(fraction)

    alert = None
    if "sangue" in request.content.lower() or "tecido" in request.content.lower():
        alert = "materia_organica_anomala"

    request.status = "concluido"

    return ResidueScanResult(
        request_id=request.id,
        fraction=fraction,
        purity=purity,
        destination=destination,
        alert=alert
    )


def assign_delivery(
    fleet: Dict[str, object],  # módulo de mobilidade
    request: LogisticsRequest
) -> DeliveryAssignment:
    """Atribui veículo para entrega de encomendas."""

    # procurar veículo operacional
    candidates = [
        v for v in fleet.values()
        if getattr(v, "status", None) == "operacional"
        and getattr(v, "ownership", None) in ("publico", "libertado")
    ]

    if not candidates:
        return DeliveryAssignment(
            request_id=request.id,
            vehicle_id=None,
            reason="Sem veículos disponíveis"
        )

    chosen = random.choice(candidates)
    chosen.status = "em_servico"

    request.status = "concluido"

    return DeliveryAssignment(
        request_id=request.id,
        vehicle_id=chosen.id,
        reason="Entrega atribuída"
    )


def process_logistics_request(
    fleet: Dict[str, object],
    request: LogisticsRequest
):
    """Processa qualquer pedido de logística."""

    if request.type == "residuo":
        return process_residue_request(request)

    if request.type == "encomenda":
        return assign_delivery(fleet, request)

    request.status = "erro"
    return None
