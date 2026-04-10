# modules/housing.py

from dataclasses import dataclass
from typing import List, Optional, Dict, Literal

from core.types import Family, House, HouseType


@dataclass
class HouseRequest:
    family_id: str
    house_id: str
    # "FIXA" ou "SUPLENTE"
    requested_type: HouseType


@dataclass
class AllocationResult:
    house_id: str
    allocated_family_id: Optional[str]
    competing_families: List[str]
    reason: str


def are_joule_credits_similar(a: float, b: float, tolerance: float = 0.05) -> bool:
    if a == 0 and b == 0:
        return True
    diff = abs(a - b)
    max_val = max(a, b)
    return True if max_val == 0 else diff / max_val <= tolerance


def has_elderly_nearby(family: Family) -> bool:
    return "idosos_presentes" in family.social_relevance_tags


def has_high_social_relevance(family: Family) -> bool:
    tags_prioritarias = {"idosos_presentes", "criancas_presentes", "cuidador", "deficiencia"}
    return any(tag in tags_prioritarias for tag in family.social_relevance_tags)


def family_has_fixed_house(family_id: str, houses: List[House]) -> bool:
    for h in houses:
        if h.type == "FIXA" and h.current_family_id == family_id:
            return True
    return False


def allocate_house(
    house: House,
    families_by_id: Dict[str, Family],
    requests: List[HouseRequest],
) -> AllocationResult:
    # filtrar pedidos para esta casa e tipo correto
    interested_families: List[Family] = []
    for r in requests:
        if r.house_id != house.id:
            continue
        fam = families_by_id.get(r.family_id)
        if fam is None:
            continue
        interested_families.append(fam)

    if not interested_families:
        return AllocationResult(
            house_id=house.id,
            allocated_family_id=None,
            competing_families=[],
            reason="Nenhuma família interessada",
        )

    if len(interested_families) == 1:
        fam = interested_families[0]
        return AllocationResult(
            house_id=house.id,
            allocated_family_id=fam.id,
            competing_families=[fam.id],
            reason="Apenas uma família interessada",
        )

    # 1) ordenar por créditos joule
    sorted_by_joule = sorted(
        interested_families,
        key=lambda f: f.joule_credits,
        reverse=True,
    )

    top = sorted_by_joule[0]
    second = sorted_by_joule[1]

    # 2) se não são semelhantes, ganha quem tem mais créditos
    if not are_joule_credits_similar(top.joule_credits, second.joule_credits):
        return AllocationResult(
            house_id=house.id,
            allocated_family_id=top.id,
            competing_families=[f.id for f in interested_families],
            reason="Maior crédito joule",
        )

    # 3) desempate por idosos
    with_elderly = [f for f in sorted_by_joule if has_elderly_nearby(f)]
    if len(with_elderly) == 1:
        return AllocationResult(
            house_id=house.id,
            allocated_family_id=with_elderly[0].id,
            competing_families=[f.id for f in interested_families],
            reason="Desempate por idosos presentes",
        )
    if len(with_elderly) > 1:
        return AllocationResult(
            house_id=house.id,
            allocated_family_id=with_elderly[0].id,
            competing_families=[f.id for f in interested_families],
            reason="Empate com idosos — escolhido o primeiro (regra a refinar)",
        )

    # 4) outras relevâncias sociais
    with_high_relevance = [f for f in sorted_by_joule if has_high_social_relevance(f)]
    if with_high_relevance:
        return AllocationResult(
            house_id=house.id,
            allocated_family_id=with_high_relevance[0].id,
            competing_families=[f.id for f in interested_families],
            reason="Desempate por relevância social",
        )

    # 5) empate total → sorteio auditável (por agora, random simples)
    import random

    chosen = random.choice(interested_families)
    return AllocationResult(
        house_id=house.id,
        allocated_family_id=chosen.id,
        competing_families=[f.id for f in interested_families],
        reason="Empate total — sorteio auditável",
    )


def assign_house(
    house: House,
    family: Family,
    all_houses: List[House],
) -> bool:
    """
    Tenta atribuir uma casa a uma família, respeitando:
    - apenas 1 casa FIXA por família
    - SUPLENTE é sempre uso, nunca posse
    """
    if house.type == "FIXA":
        if family_has_fixed_house(family.id, all_houses):
            return False
        house.current_family_id = family.id
        return True

    if house.type == "SUPLENTE":
        house.current_family_id = family.id
        return True

    return False


def release_supplement_house(house: House, family_id: str) -> bool:
    """
    Liberta uma casa suplente quando a família sai.
    """
    if house.type != "SUPLENTE":
        return False
    if house.current_family_id != family_id:
        return False
    house.current_family_id = None
    return True
