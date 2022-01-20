import BISList from './bis_list'
import { Character } from './character'

export default interface TeamMember {
  bis_list: BISList
  character: Character
  id: number
  lead: boolean
}
