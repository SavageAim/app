import Team from './team'

export interface GreedItem {
  bis_list_id: number
  current_gear_name: string
  current_gear_il: number
  job_icon_name: string
  job_role: string
}

export interface GreedGear {
  member_id: number
  character_name: string
  greed_lists: GreedItem[]
}

export interface NeedGear {
  member_id: number
  character_name: string
  current_gear_name: string
  current_gear_il: number
  job_icon_name: string
  job_role: string
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
}

interface Loot {
  greed: boolean
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

export interface LootPacket {
  greed: boolean
  greed_bis_id: number | null
  item: string
  member_id: number
}
