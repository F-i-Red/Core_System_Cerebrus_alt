// core/types.ts

export type PersonId = string;
export type FamilyId = string;
export type BlockId = string;
export type HouseId = string;

export type ActivityStatus = 'ATIVO' | 'INATIVO' | 'FORA_DA_REDE';

export interface Person {
  id: PersonId;
  name: string;
  age: number;
  activityStatus: ActivityStatus;
  // ex: "idoso", "criança", "adulto", "cuidador", etc.
  socialRoleTags: string[];
  familyId: FamilyId;
}

export interface Family {
  id: FamilyId;
  members: PersonId[];
  // créditos joule disponíveis para decisões (habitação, mobilidade, etc.)
  jouleCredits: number;
  // ex: "idosos_presentes", "crianças_presentes", "cuidador", etc.
  socialRelevanceTags: string[];
}

export interface Block {
  id: BlockId;
  name: string;
  houses: HouseId[];
}

export type HouseType = 'FIXA' | 'SUPLENTE';

export interface House {
  id: HouseId;
  blockId: BlockId;
  type: HouseType;
  capacity: number;
  // família atual (se houver)
  currentFamilyId?: FamilyId;
  // se é acessível para idosos, mobilidade reduzida, etc.
  accessibilityTags: string[];
}
