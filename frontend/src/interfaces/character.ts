import BISList from './bis_list'

interface BISSummary {
  name: string
  id: number
}

export interface Character {
  alias: string
  avatar_url: string
  id: number
  lodestone_id: string
  proxy: boolean
  name: string
  user_id: number
  verified: boolean
  world: string
  bis_lists: BISSummary[]
}

// The detailed view of a character's information
export interface CharacterDetails extends Character {
  // TODO - Add arrays for gearsets and teams and stuff
  bis_lists: BISList[]
  token: string
}
