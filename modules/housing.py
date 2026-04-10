# modules/housing.py

from dataclasses import dataclass
from typing import List, Optional, Dict

from core.types import Family, House


@dataclass
class HouseRequest:
    family_id: str
    house_id: str


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


def allocate_house(
    house: House,
    families_by_id: Dict[str, Family],
    requests: List[HouseRequest],
) -> AllocationResult:
    interested_families: List[Family] = [
        families_by_id[r.family_id]
        for r in requests
        if r.house_id == house.id and r.family_id in families_by_id
    ]

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
        # podemos refinar depois (idade média, nº de idosos, etc.)
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
