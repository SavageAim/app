export interface FirstFloor {
  earrings: number | null
  necklace: number | null
  bracelet: number | null
  ring: number | null
  token: boolean
}

export interface SecondFloor {
  head: number | null
  hands: number | null
  feet: number | null
  'tome-accessory-augment': number | null
  token: boolean
}

export interface ThirdFloor {
  body: number | null
  legs: number | null
  'tome-armour-augment': number | null
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
