export interface FirstFloor {
  Earrings: number | null
  Necklace: number | null
  Bracelet: number | null
  Ring: number | null
  token: boolean
}

export interface SecondFloor {
  Head: number | null
  Hands: number | null
  Feet: number | null
  'Tome Accessory Augment': number | null
  token: boolean
}

export interface ThirdFloor {
  Body: number | null
  Legs: number | null
  'Tome Armour Augment': number | null
  token: boolean
}

export interface FourthFloor {
  weapons: number
  mounts: number
}

export interface LootSolverData {
  first_floor: FirstFloor[]
  second_floor: SecondFloor[]
  third_floor: ThirdFloor[]
  fourth_floor: FourthFloor
}
