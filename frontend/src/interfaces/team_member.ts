import BISList from './bis_list'
import { Character } from './character'

interface Permissions {
  loot_manager: boolean
  team_characters: boolean
}

export default interface TeamMember {
  bis_list: BISList
  character: Character
  id: number
  lead: boolean
  name: string
  permissions: Permissions
}
