<template>
  <div class="box">
    <div class="level">
      <div class="media-left">
        <div class="level-item">
          {{ member.name }}
        </div>
      </div>
      <div class="level-right">
        <div class="level-item">
          <div class="tags is-grouped is-grouped-multiline">
            <template v-if="member.lead">
              <span class="tag is-primary">Leader</span>
            </template>
            <template v-else>
              <span class="tag is-info" v-if="member.permissions.loot_manager">Loot Manager</span>
              <span class="tag is-info" v-if="member.permissions.proxy_manager">Proxy Manager</span>
            </template>
          </div>
        </div>
      </div>
    </div>
    <div class="buttons is-grouped" v-if="userIsLead && !member.lead">
      <button class="button is-primary is-outlined is-fullwidth">
        <span>Edit Permissions</span>
      </button>
      <button class="button is-danger is-outlined is-fullwidth" @click="kick">
        <span>Kick From Team</span>
      </button>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'
import KickFromTeam from '@/components/modals/confirmations/kick_from_team.vue'
import TeamMember from '@/interfaces/team_member'

@Component
export default class TeamMemberManager extends Vue {
  @Prop()
  userIsLead!: boolean

  @Prop()
  member!: TeamMember

  kick(): void {
    this.$modal.show(KickFromTeam, { details: this.member, teamId: this.$route.params.id }, { }, { closed: () => { this.$emit('reload') } })
  }
}
</script>

<style lang="scss">

</style>
