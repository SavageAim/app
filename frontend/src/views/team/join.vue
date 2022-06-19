<template>
  <div>
    <div v-if="!teamLoaded">
      <button class="button is-static is-loading is-fullwidth">Loading</button>
    </div>

    <template v-else>
      <div class="breadcrumb">
        <ul>
          <li><router-link to="/team/">Create or Join a Team</router-link></li>
          <li class="is-active"><a>Join a Team</a></li>
        </ul>
      </div>

      <div class="container">
        <!-- Team display box here -->
        <div class="card">
          <div class="card-header">
            <div class="card-header-title">You have been invited to join;</div>
          </div>
          <div class="card-content">
            <div class="box">
              <TeamBio :team="team" :displayIcons="false" />
            </div>
          </div>
        </div>

        <div class="card">
          <div class="card-header">
            <div class="card-header-title">Select your Character and BIS List</div>
          </div>
          <div class="card-content">
            <TeamMemberForm ref="form" :bis-list-id-errors="errors.bis_list_id" :character-id-errors="errors.character_id" />
            <button class="button is-success" @click="join">Join!</button>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import TeamBio from '@/components/team_bio.vue'
import TeamMemberForm from '@/components/team/member_form.vue'
import { TeamCreateResponse, TeamMemberUpdateErrors } from '@/interfaces/responses'
import Team from '@/interfaces/team'
import SavageAimMixin from '@/mixins/savage_aim_mixin'

@Component({
  components: {
    TeamBio,
    TeamMemberForm,
  },
})
export default class TeamJoin extends SavageAimMixin {
  teamLoaded = false

  errors: TeamMemberUpdateErrors = {}

  team!: Team

  // Values for sending
  get bisListId(): string {
    return (this.$refs.form as TeamMemberForm).bisListId
  }

  get characterId(): string {
    return (this.$refs.form as TeamMemberForm).characterId
  }

  get url(): string {
    return `/backend/api/team/join/${this.$route.params.id}/`
  }

  created(): void {
    this.fetchTeam()
  }

  async fetchTeam(): Promise<void> {
    // Load the team data from the API
    try {
      const response = await fetch(this.url)
      if (response.ok) {
        // Parse the JSON into a team and save it
        this.team = (await response.json()) as Team
        this.teamLoaded = true
        document.title = `Join ${this.team.name} - Savage Aim`
      }
      else if (response.status === 404) {
        // Handle 404s ourselves to go back to the create/join page with a warning
        this.$router.push('/team/', () => {
          Vue.notify({ text: 'Invalid invite code! Please make sure you copied it correctly!', type: 'is-danger' })
        })
      }
      else {
        super.handleError(response.status)
      }
    }
    catch (e) {
      this.$notify({ text: `Error ${e} when fetching Team.`, type: 'is-danger' })
    }
  }

  async join(): Promise<void> {
    this.errors = {}

    const body = JSON.stringify({ bis_list_id: this.bisListId, character_id: this.characterId })
    try {
      const response = await fetch(this.url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': this.$cookies.get('csrftoken'),
        },
        body,
      })

      if (response.ok) {
        // Redirect back to the new bis list page
        const json = await response.json() as TeamCreateResponse
        this.$store.dispatch('fetchTeams')
        this.$router.push(`/team/${json.id}/`, () => {
          Vue.notify({ text: `Welcome to ${this.team.name}!`, type: 'is-success' })
        })
      }
      else {
        super.handleError(response.status)
        this.errors = (await response.json() as TeamMemberUpdateErrors)
      }
    }
    catch (e) {
      this.$notify({ text: `Error ${e} when attempting to create BIS List.`, type: 'is-danger' })
    }
  }
}
</script>

<style lang="scss">
</style>
