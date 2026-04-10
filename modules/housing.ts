// modules/housing.ts

import { Family, House, HouseId, FamilyId } from '../core/types';

interface HouseRequest {
  familyId: FamilyId;
  houseId: HouseId;
}

interface AllocationResult {
  houseId: HouseId;
  allocatedFamilyId: FamilyId | null;
  competingFamilies: FamilyId[];
  reason: string;
}

function areJouleCreditsSimilar(a: number, b: number, tolerance: number = 0.05): boolean {
  if (a === 0 && b === 0) return true;
  const diff = Math.abs(a - b);
  const max = Math.max(a, b);
  return max === 0 ? true : diff / max <= tolerance;
}

function hasElderlyNearby(family: Family): boolean {
  return family.socialRelevanceTags.includes('idosos_presentes');
}

function hasHighSocialRelevance(family: Family): boolean {
  // aqui podemos ir afinando: cuidadores, pessoas com deficiência, etc.
  return family.socialRelevanceTags.some(tag =>
    ['idosos_presentes', 'crianças_presentes', 'cuidador', 'deficiencia'].includes(tag)
  );
}

export function allocateHouse(
  house: House,
  families: Family[],
  requests: HouseRequest[]
): AllocationResult {
  const interestedFamilies = requests
    .filter(r => r.houseId === house.id)
    .map(r => families.find(f => f.id === r.familyId))
    .filter((f): f is Family => !!f);

  if (interestedFamilies.length === 0) {
    return {
      houseId: house.id,
      allocatedFamilyId: null,
      competingFamilies: [],
      reason: 'Nenhuma família interessada'
    };
  }

  if (interestedFamilies.length === 1) {
    return {
      houseId: house.id,
      allocatedFamilyId: interestedFamilies[0].id,
      competingFamilies: [interestedFamilies[0].id],
      reason: 'Apenas uma família interessada'
    };
  }

  // 1) ordenar por créditos joule
  const sortedByJoule = [...interestedFamilies].sort(
    (a, b) => b.jouleCredits - a.jouleCredits
  );

  const top = sortedByJoule[0];
  const second = sortedByJoule[1];

  // 2) verificar se são semelhantes em créditos
  if (!areJouleCreditsSimilar(top.jouleCredits, second.jouleCredits)) {
    return {
      houseId: house.id,
      allocatedFamilyId: top.id,
      competingFamilies: interestedFamilies.map(f => f.id),
      reason: 'Maior crédito joule'
    };
  }

  // 3) desempate por relevância social (idosos, etc.)
  const withElderly = sortedByJoule.filter(hasElderlyNearby);
  if (withElderly.length === 1) {
    return {
      houseId: house.id,
      allocatedFamilyId: withElderly[0].id,
      competingFamilies: interestedFamilies.map(f => f.id),
      reason: 'Desempate por idosos presentes'
    };
  }

  if (withElderly.length > 1) {
    // ainda empatados: podemos refinar mais tarde (ex: mais idade média, etc.)
    return {
      houseId: house.id,
      allocatedFamilyId: withElderly[0].id,
      competingFamilies: interestedFamilies.map(f => f.id),
      reason: 'Empate com idosos — escolhido o primeiro por agora (regra a refinar)'
    };
  }

  // 4) outras relevâncias sociais
  const withHighRelevance = sortedByJoule.filter(hasHighSocialRelevance);
  if (withHighRelevance.length > 0) {
    return {
      houseId: house.id,
      allocatedFamilyId: withHighRelevance[0].id,
      competingFamilies: interestedFamilies.map(f => f.id),
      reason: 'Desempate por relevância social'
    };
  }

  // 5) se ainda assim empatar, podemos usar sorteio auditável
  const randomIndex = Math.floor(Math.random() * interestedFamilies.length);
  const chosen = interestedFamilies[randomIndex];

  return {
    houseId: house.id,
    allocatedFamilyId: chosen.id,
    competingFamilies: interestedFamilies.map(f => f.id),
    reason: 'Empate total — sorteio auditável'
  };
}
