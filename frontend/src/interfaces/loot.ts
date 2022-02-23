import Team from './team'

export interface GreedItem {
  bis_list_id: number
  current_gear_name: string
  current_gear_il: number
  job_icon_name: string
  job_role: string
}

export interface TomeGreedItem {
  bis_list_id: number
  job_icon_name: string
  job_role: string
  required: number
}

export interface GreedGear {
  member_id: number
  character_name: string
  greed_lists: GreedItem[]
}

export interface TomeGreedGear {
  member_id: number
  character_name: string
  greed_lists: TomeGreedItem[]
}

export interface NeedGear {
  member_id: number
  character_name: string
  current_gear_name: string
  current_gear_il: number
  job_icon_name: string
  job_role: string
}

export interface TomeNeedGear {
  member_id: number
  character_name: string
  job_icon_name: string
  job_role: string
  required: number
}

interface LootGear {
  mainhand: { need: NeedGear[], greed: GreedGear[] }
  offhand: { need: NeedGear[], greed: GreedGear[] }
  head: { need: NeedGear[], greed: GreedGear[] }
  body: { need: NeedGear[], greed: GreedGear[] }
  hands: { need: NeedGear[], greed: GreedGear[] }
  legs: { need: NeedGear[], greed: GreedGear[] }
  feet: { need: NeedGear[], greed: GreedGear[] }
  earrings: { need: NeedGear[], greed: GreedGear[] }
  necklace: { need: NeedGear[], greed: GreedGear[] }
  bracelet: { need: NeedGear[], greed: GreedGear[] }
  ring: { need: NeedGear[], greed: GreedGear[] }
  'tome-accessory-augment': { need: TomeNeedGear[], greed: TomeGreedGear[] }
  'tome-armour-augment': { need: TomeNeedGear[], greed: TomeGreedGear[] }
}

export interface Loot {
  greed: boolean
  id: number
  item: string
  member: string
  obtained: string
}

export interface LootData {
  gear: LootGear
  history: Loot[]
}

export interface LootResponse {
  loot: LootData
  team: Team
}

export interface LootWithBISPacket {
  greed: boolean
  greed_bis_id: number | null
  item: string
  member_id: number
}

export interface LootPacket {
  greed: boolean
  item: string
  member_id: number
  obtained: string
}
