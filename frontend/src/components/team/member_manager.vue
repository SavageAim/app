<template>
  <div class="box">
    <div class="member-name">
      {{ member.name }}
    </div>
    <div class="permission-tags">
      <div class="tags">
        <template v-if="member.lead">
          <span class="tag is-primary">Leader</span>
        </template>
        <template v-else>
          <span class="tag is-info" v-if="member.permissions.loot_manager">Loot Manager</span>
          <span class="tag is-info" v-if="member.permissions.proxy_manager">Proxy Manager</span>
        </template>
      </div>
    </div>
    <div class="management-buttons buttons is-grouped" v-if="userIsLead && !member.lead">
      <button class="button is-primary is-outlined is-fullwidth" @click="editPermissions">
        <span class="icon"><i class="material-icons">edit</i></span>
        <span>Edit Permissions</span>
      </button>
      <button class="button is-danger is-outlined is-fullwidth" @click="kick">
        <span class="icon"><i class="material-icons">delete</i></span>
        <span>Kick From Team</span>
      </button>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'
import KickFromTeam from '@/components/modals/confirmations/kick_from_team.vue'
import Permissions from '@/components/modals/permissions.vue'
import TeamMember from '@/interfaces/team_member'

@Component
export default class TeamMemberManager extends Vue {
  @Prop()
  member!: TeamMember

  @Prop()
  teamId!: string

  @Prop()
  userIsLead!: boolean

  editPermissions(): void {
    this.$modal.show(Permissions, { member: this.member, teamId: this.teamId }, { }, { closed: () => { this.$emit('reload') } })
  }

  kick(): void {
    this.$modal.show(KickFromTeam, { details: this.member, teamId: this.teamId }, { }, { closed: () => { this.$emit('reload') } })
  }
}
</script>

<style lang="scss">
.permission-tags {
  margin-top: 0.25rem;
}

.management-buttons {
  margin-top: 1rem;
}

@media screen and (min-width: 1024px) {
  .member-name {
    display: inline-block;
  }

  .permission-tags {
    margin-top: 0;
    display: inline-block;
    float: right;
  }
}
</style>
