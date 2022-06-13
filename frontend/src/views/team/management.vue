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
            <TeamNav :editable="editable" />
          </div>
        </div>
      </div>

      <div class="container is-fluid">
        <div class="card">
          <div class="card-header">
            <div class="card-header-title">
              Member Permissions
            </div>
          </div>
          <div class="card-content">
            <table class="table is-fullwidth is-bordered">
              <thead>
                <tr>
                  <th></th>
                  <th class="has-text-centered">Loot Manager Control</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="member in team.members" :key="member.id">
                  <th>{{ member.name }}</th>
                  <td class="has-text-centered"><input type="checkbox" /></td>
                </tr>
              </tbody>
            </table>
          </div>
          <div class="card-footer">
            <a class="has-text-success card-footer-item">Save</a>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script lang="ts">
import { Component } from 'vue-property-decorator'
import TeamNav from '@/components/team_nav.vue'
import { TeamUpdateErrors } from '@/interfaces/responses'
import Team from '@/interfaces/team'
import TeamMember from '@/interfaces/team_member'
import SavageAimMixin from '@/mixins/savage_aim_mixin'

@Component({
  components: {
    TeamNav,
  },
})
export default class TeamManagement extends SavageAimMixin {
  errors: TeamUpdateErrors = {}

  firstLoad = true

  loading = true

  teamLeadId!: number

  team!: Team

  // Flag stating whether the currently logged user can edit the Team
  editable(): boolean {
    return this.team.members.find((teamMember: TeamMember) => teamMember.character.user_id === this.$store.state.user.id)?.lead ?? false
  }

  get url(): string {
    return `/backend/api/team/${this.$route.params.id}/`
  }

  created(): void {
    this.fetchTeam(false)
  }

  async fetchTeam(reload: boolean): Promise<void> {
    // Load the team data from the API
    try {
      const response = await fetch(this.url)
      if (response.ok) {
        // Parse the JSON into a team and save it
        this.team = (await response.json()) as Team
        this.loading = false
        this.firstLoad = false
        if (reload) this.$forceUpdate()
        document.title = `Management - ${this.team.name} - Savage Aim`
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
