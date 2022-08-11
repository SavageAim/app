// Not your standard mixin, needs to be extended
import Team from '@/interfaces/team'
import TeamMember from '@/interfaces/team_member'
import SavageAimMixin from '@/mixins/savage_aim_mixin'

export default class TeamViewMixin extends SavageAimMixin {
  team!: Team

  // Flag stating whether the currently logged user can control the Loot Manager
  get userHasLootManagerPermission(): boolean {
    return this.team.members
      .filter((teamMember: TeamMember) => teamMember.permissions.loot_manager)
      .some((teamMember: TeamMember) => teamMember.character.user_id === this.$store.state.user.id)
  }

  // Flag stating whether the currently logged user can manage Proxy Chars
  get userHasProxyManagerPermission(): boolean {
    return this.team.members
      .filter((teamMember: TeamMember) => teamMember.permissions.proxy_manager)
      .some((teamMember: TeamMember) => teamMember.character.user_id === this.$store.state.user.id)
  }

  // Flag stating whether the currently logged user is the leader of the team
  get userIsTeamLead(): boolean {
    return this.team.members
      .filter((teamMember: TeamMember) => teamMember.lead)
      .some((teamMember: TeamMember) => teamMember.character.user_id === this.$store.state.user.id)
  }
}
