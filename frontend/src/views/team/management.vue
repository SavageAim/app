<template>
  <div>
    <div v-if="loading">
      <button class="button is-static is-loading is-fullwidth">Loading</button>
    </div>

    <template v-else>
      <div class="level">
        <div class="level-left">
          <div class="level-item">
            <h2 class="title is-spaced">{{ team.name }}</h2>
            <div class="icon-text subtitle is-hidden-touch">
              <span class="icon"><i class="material-icons">room</i></span>
              <span>{{ team.tier.name }}</span>
            </div>
          </div>
        </div>

        <div class="level-right">
          <div class="level-item">
            <TeamNav :is-lead="userIsTeamLead" />
          </div>
        </div>
      </div>

      <!-- Main body of page -->
      <div class="columns">
        <div class="column">
          <div class="card">
            <div class="card-header">
              <div class="card-header-title">Team Members</div>
            </div>
            <div class="card-content">
              <TeamMemberManager :member="member" :user-is-lead="userIsTeamLead" v-for="member in realMembers()" :key="member.id" v-on:reload="() => { fetchTeam(true) }" />
            </div>
          </div>
        </div>

        <div class="column">
          <div class="card">
            <div class="card-header">
              <div class="card-header-title">Proxy Characters</div>
              <!-- Replace with check for the perm -->
              <div class="card-header-icon" v-if="userHasProxyManagerPermission">
                <router-link to="../proxies/" class="button is-small is-success">
                  <span>Add Proxy Character</span>
                </router-link>
              </div>
            </div>
            <div class="card-content">
              <ProxyMemberManager :member="member" :user-has-permission="userHasProxyManagerPermission" v-for="member in proxyMembers()" :key="member.id" v-on:reload="() => { fetchTeam(true) }" />
            </div>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script lang="ts">
import { Component } from 'vue-property-decorator'
import TeamMemberManager from '@/components/team/member_manager.vue'
import TeamNav from '@/components/team/nav.vue'
import ProxyMemberManager from '@/components/team/proxy_manager.vue'
import Team from '@/interfaces/team'
import TeamMember from '@/interfaces/team_member'
import TeamViewMixin from '@/mixins/team_view_mixin'

@Component({
  components: {
    TeamMemberManager,
    TeamNav,
    ProxyMemberManager,
  },
})
export default class TeamManagement extends TeamViewMixin {
  loading = true

  team!: Team

  get url(): string {
    return `/backend/api/team/${this.$route.params.id}/`
  }

  // Retrieve the User's Character in the Team
  get userMember(): TeamMember | undefined {
    return this.team.members.find((teamMember: TeamMember) => teamMember.character.user_id === this.$store.state.user.id)
  }

  created(): void {
    this.fetchTeam(false)
  }

  proxyMembers(): TeamMember[] {
    return this.team.members.filter((tm: TeamMember) => tm.character.proxy)
  }

  realMembers(): TeamMember[] {
    return this.team.members.filter((tm: TeamMember) => !tm.character.proxy)
  }

  async fetchTeam(reload: boolean): Promise<void> {
    // Load the team data from the API
    try {
      const response = await fetch(this.url)
      if (response.ok) {
        // Parse the JSON into a team and save it
        this.team = (await response.json()) as Team
        this.loading = false
        if (reload) this.$forceUpdate()
        document.title = `Manage Members - ${this.team.name} - Savage Aim`
      }
      else {
        super.handleError(response.status)
      }
    }
    catch (e) {
      this.$notify({ text: `Error ${e} when fetching Team.`, type: 'is-danger' })
    }
  }

  async load(): Promise<void> {
    this.fetchTeam(true)
  }
}
</script>

<style lang="scss">

</style>
