import BISList from './bis_list'

export interface Character {
  id: number
  avatar_url: string
  lodestone_id: string
  name: string
  user_id: number
  verified: boolean
  world: string
}

// The detailed view of a character's information
export interface CharacterDetails extends Character {
  // TODO - Add arrays for gearsets and teams and stuff
  bis_lists: BISList[]
  token: string

}
