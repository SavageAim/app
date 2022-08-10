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
              <span class="tag is-info" v-if="lootManager">Loot Manager</span>
              <span class="tag is-info" v-if="proxyManager">Proxy Manager</span>
            </template>
          </div>
        </div>
      </div>
    </div>
    <div class="buttons is-grouped" v-if="isLead && !member.lead">
      <button class="button is-primary is-outlined is-fullwidth">
        <span>Edit Permissions</span>
      </button>
      <button class="button is-danger is-outlined is-fullwidth">
        <span>Kick From Team</span>
      </button>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'
import TeamMember from '@/interfaces/team_member'

@Component
export default class TeamMemberManager extends Vue {
  @Prop()
  isLead!: boolean

  @Prop()
  member!: TeamMember

  @Prop()
  permissions!: number

  get lootManager(): boolean {
    // Determine if the character can use the loot manager (1st bit of the permission number)
    return (this.permissions & 1) === 1
  }

  get proxyManager(): boolean {
    // Determine if the character can manage proxies (2nd bit of the permission number)
    return (this.permissions & 2) === 2
  }
}
</script>

<style lang="scss">

</style>
