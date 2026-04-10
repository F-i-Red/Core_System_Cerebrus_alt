# core/types.py

from dataclasses import dataclass
from typing import List, Optional, Literal

ActivityStatus = Literal["ATIVO", "INATIVO", "FORA_DA_REDE"]
HouseType = Literal["FIXA", "SUPLENTE"]


@dataclass
class Person:
    id: str
    name: str
    age: int
    activity_status: ActivityStatus
    # ex: "idoso", "crianca", "adulto", "cuidador"
    social_role_tags: List[str]
    family_id: str


@dataclass
class Family:
    id: str
    members: List[str]  # lista de Person.id
    joule_credits: float
    # ex: "idosos_presentes", "criancas_presentes", "cuidador", "deficiencia"
    social_relevance_tags: List[str]


# core/types.py (só este detalhe)

@dataclass
class House:
    id: str
    block_id: str
    type: HouseType
    capacity: int
    current_family_id: Optional[str] = None
    accessibility_tags: List[str] = None

    def __post_init__(self):
        if self.accessibility_tags is None:
            self.accessibility_tags = []

