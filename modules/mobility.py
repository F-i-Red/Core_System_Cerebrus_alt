# modules/mobility.py

from dataclasses import dataclass
from typing import List, Dict, Optional, Literal
import random

VehicleStatus = Literal[
    "operacional",
    "em_servico",
    "avariado",
    "em_reboque",
    "em_manutencao",
    "fora_de_servico"
]

VehicleType = Literal[
    "carro_autonomo",
    "bicicleta",
    "barco_autonomo",
    "drone",
    "reboque",
    "super_reboque"
]

Ownership = Literal["publico", "privado", "libertado", "reciclado"]


@dataclass
class Vehicle:
    id: str
    type: VehicleType
    status: VehicleStatus
    ownership: Ownership
    location: str  # nome do bloco ou ponto
    battery: float = 100.0  # %


@dataclass
class MobilityRequest:
    person_id: str
    origin: str
    destination: str
    priority: int  # 0 normal, 1 idosos, 2 emergência, 3 Força Cívica


@dataclass
class MobilityAssignment:
    vehicle_id: Optional[str]
    reason: str


# --------------------------
# Funções internas
# --------------------------

def find_available_vehicle(fleet: Dict[str, Vehicle], origin: str) -> Optional[Vehicle]:
    """Escolhe o veículo operacional mais próximo (simplificado)."""
    candidates = [
        v for v in fleet.values()
        if v.status == "operacional" and v.ownership in ("publico", "libertado")
    ]
    if not candidates:
        return None
    return random.choice(candidates)


def find_reboque(fleet: Dict[str, Vehicle]) -> Optional[Vehicle]:
    """Procura um reboque disponível."""
    for v in fleet.values():
        if v.type == "reboque" and v.status == "operacional":
            return v
    return None


def find_super_reboque(fleet: Dict[str, Vehicle]) -> Optional[Vehicle]:
    """Reboque dos reboques — raro."""
    for v in fleet.values():
        if v.type == "super_reboque" and v.status == "operacional":
            return v
    return None


# --------------------------
# API principal do módulo
# --------------------------

def request_vehicle(
    fleet: Dict[str, Vehicle],
    req: MobilityRequest
) -> MobilityAssignment:
    """Pedido normal de mobilidade."""

    # prioridade alta → tentar veículo imediatamente
    vehicle = find_available_vehicle(fleet, req.origin)

    if vehicle:
        vehicle.status = "em_servico"
        return MobilityAssignment(vehicle_id=vehicle.id, reason="Veículo atribuído")

    # sem veículos → tentar redundância
    return MobilityAssignment(vehicle_id=None, reason="Sem veículos disponíveis")


def handle_breakdown(
    fleet: Dict[str, Vehicle],
    vehicle_id: str
) -> str:
    """Processa avaria e ativa redundância."""

    if vehicle_id not in fleet:
        return "Veículo inexistente"

    vehicle = fleet[vehicle_id]
    vehicle.status = "avariado"

    # 1) chamar reboque
    reboque = find_reboque(fleet)
    if reboque:
        reboque.status = "em_servico"
        vehicle.status = "em_reboque"
        return f"Reboque {reboque.id} enviado para {vehicle.id}"

    # 2) se o reboque também falhar → super reboque
    super_r = find_super_reboque(fleet)
    if super_r:
        super_r.status = "em_servico"
        vehicle.status = "em_reboque"
        return f"Super-reboque {super_r.id} enviado para {vehicle.id}"

    # 3) falha total (muito raro)
    return "Falha crítica: nenhum reboque disponível"


def return_to_base_for_maintenance(
    fleet: Dict[str, Vehicle],
    vehicle_id: str,
    base: str
) -> str:
    """Veículo regressa ao ponto de recolha para manutenção."""

    if vehicle_id not in fleet:
        return "Veículo inexistente"

    v = fleet[vehicle_id]
    v.status = "em_manutencao"
    v.location = base
    v.battery = 100.0

    return f"{v.id} em manutenção no ponto {base}"


# --------------------------
# Gestão de carros privados
# --------------------------

def register_private_vehicle(fleet: Dict[str, Vehicle], vehicle: Vehicle) -> None:
    fleet[vehicle.id] = vehicle


def liberate_private_vehicle(fleet: Dict[str, Vehicle], vehicle_id: str) -> str:
    if vehicle_id not in fleet:
        return "Veículo inexistente"
    v = fleet[vehicle_id]
    v.ownership = "libertado"
    return f"Veículo {vehicle_id} libertado para o sistema"


def recycle_private_vehicle(fleet: Dict[str, Vehicle], vehicle_id: str) -> str:
    if vehicle_id not in fleet:
        return "Veículo inexistente"
    v = fleet[vehicle_id]
    v.ownership = "reciclado"
    v.status = "fora_de_servico"
    return f"Veículo {vehicle_id} reciclado e removido da frota ativa"
