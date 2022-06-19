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

      <div class="container">
        <div class="card">
          <div class="card-header">
            <div class="card-header-title">Invite Code</div>
          </div>
          <div class="card-content">
            <div class="field has-addons">
              <div class="control is-expanded">
                <input class="input" id="inviteCode" type="text" :value="team.invite_code" readonly />
              </div>
              <label class="label is-sr-only" for="inviteCode">Invite Code</label>
              <div class="control">
                <button class="button is-warning" @click="regenerateInviteCode">Regenerate</button>
              </div>
            </div>
            <p>Send the above code, or <a :href="`${inviteUrl}/${team.invite_code}/`" target="_blank">this URL</a>, to people to allow them to join <span class="has-text-primary">{{ team.name }}</span>!</p>
          </div>
        </div>

        <div class="card">
          <div class="card-header">
            <div class="card-header-title">Settings</div>
          </div>

          <div class="card-content">
            <div class="field">
              <label class="label" for="teamName">Team Name</label>
              <div class="control">
                <input class="input" id="teamName" type="text" placeholder="Team Name" v-model="team.name" :class="{'is-danger': errors.name !== undefined}" />
              </div>
              <p v-if="errors.name !== undefined" class="help is-danger">{{ errors.name[0] }}</p>
            </div>

            <div class="field">
              <label class="label" for="tier">Tier</label>
              <div class="select is-fullwidth" :class="{'is-danger': errors.tier_id !== undefined}">
                <select v-model="team.tier.id" id="tier">
                  <option v-for="tier in $store.state.tiers" :key="tier.id" :value="tier.id">{{ tier.name }}</option>
                </select>
              </div>
              <p v-if="errors.tier_id !== undefined" class="help is-danger">{{ errors.tier_id[0] }}</p>
            </div>
            <hr />
            <div class="field">
              <label class="label has-text-warning" for="teamLead">Team Lead</label>
              <div class="select is-fullwidth" :class="[errors.team_lead !== undefined ? 'is-danger' : 'is-warning']">
                <select v-model="teamLeadId" id="teamLead">
                  <option v-for="member in team.members" :key="member.id" :value="member.character.id">{{ member.name }}</option>
                </select>
              </div>
              <p class="help is-warning">Changing this will lock you out of this page. Please be sure you want to hand over leadership before changing this value.</p>
              <p v-if="errors.team_lead !== undefined" class="help is-danger">{{ errors.team_lead[0] }}</p>
            </div>
          </div>
          <footer class="card-footer">
            <a class="has-text-success card-footer-item" @click="saveDetails">Save</a>
            <a class="has-text-danger card-footer-item" @click="disband">Disband</a>
          </footer>
        </div>
      </div>
    </template>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import TeamNav from '@/components/team/nav.vue'
import DeleteTeam from '@/components/modals/confirmations/delete_team.vue'
import { TeamUpdateErrors } from '@/interfaces/responses'
import Team from '@/interfaces/team'
import TeamMember from '@/interfaces/team_member'
import SavageAimMixin from '@/mixins/savage_aim_mixin'

@Component({
  components: {
    TeamNav,
  },
})
export default class TeamSettings extends SavageAimMixin {
  errors: TeamUpdateErrors = {}

  firstLoad = true

  loading = true

  teamLeadId!: number

  team!: Team

  // Flag stating whether the currently logged user can edit the Team
  editable(): boolean {
    return this.team.members.find((teamMember: TeamMember) => teamMember.character.user_id === this.$store.state.user.id)?.lead ?? false
  }

  get inviteUrl(): string {
    return `${process.env.VUE_APP_URL}/team/join`
  }

  get url(): string {
    return `/backend/api/team/${this.$route.params.id}/`
  }

  checkPermissions(displayWarning: boolean): void {
    // Ensure that the person on this page is the team leader and not anybody else
    if (!this.editable()) {
      this.$router.push(`/team/${this.$route.params.id}/`, () => {
        if (displayWarning) Vue.notify({ text: 'Only the team leader can edit a Team\'s settings.', type: 'is-warning' })
      })
    }
  }

  created(): void {
    this.fetchTeam(false)
  }

  disband(): void {
    this.$modal.show(DeleteTeam, { team: this.team })
  }

  async fetchTeam(reload: boolean): Promise<void> {
    // Load the team data from the API
    try {
      const response = await fetch(this.url)
      if (response.ok) {
        // Parse the JSON into a team and save it
        this.team = (await response.json()) as Team
        this.checkPermissions(this.firstLoad)
        this.teamLeadId = this.team.members.find((teamMember: TeamMember) => teamMember.character.user_id === this.$store.state.user.id)?.character.id ?? -1
        this.loading = false
        this.firstLoad = false
        if (reload) this.$forceUpdate()
        document.title = `Settings - ${this.team.name} - Savage Aim`
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

  async regenerateInviteCode(): Promise<void> {
    try {
      const response = await fetch(this.url, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': this.$cookies.get('csrftoken'),
        },
      })

      if (response.ok) {
        this.$notify({ text: 'New Invite Code Generated!', type: 'is-success' })
        await this.fetchTeam(true)
      }
      else {
        super.handleError(response.status)
      }
    }
    catch (e) {
      this.$notify({ text: `Error ${e} when attempting to regenerate Team Invite Code.`, type: 'is-danger' })
    }
  }

  async saveDetails(): Promise<void> {
    const updateObj = {
      name: this.team.name,
      tier_id: this.team.tier.id,
      team_lead: this.teamLeadId,
    }

    try {
      const response = await fetch(this.url, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': this.$cookies.get('csrftoken'),
        },
        body: JSON.stringify(updateObj),
      })

      if (response.ok) {
        this.$notify({ text: 'Successfully updated!', type: 'is-success' })
        await this.fetchTeam(true)
      }
      else {
        super.handleError(response.status)
        this.errors = (await response.json() as TeamUpdateErrors)
      }
    }
    catch (e) {
      this.$notify({ text: `Error ${e} when attempting to update Team settings.`, type: 'is-danger' })
    }
  }
}
</script>

<style lang="scss">
</style>
