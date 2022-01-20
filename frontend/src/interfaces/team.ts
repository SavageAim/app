import TeamMember from './team_member'
import Tier from './tier'

export default interface Team {
  id: string
  members: TeamMember[]
  invite_code: string
  name: string
  tier: Tier
}
