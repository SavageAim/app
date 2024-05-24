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
            <TeamNav :is-lead="userIsTeamLead" :team-id="teamId" />
          </div>
        </div>
      </div>

      <div class="container is-fluid">
        <div class="card">
          <div class="card-header">
            <div class="card-header-title">Invite Code</div>
          </div>
          <div class="card-content">
            <div class="field has-addons">
              <div class="control is-expanded">
                <input class="input is-dark" id="inviteCode" type="text" :value="team.invite_code" readonly />
              </div>
              <label class="label is-sr-only" for="inviteCode">Invite Code</label>
              <div class="control">
                <button class="button is-dark" @click="regenerateInviteCode">Regenerate</button>
              </div>
            </div>
            <p>Send the above code, or <a :href="`${inviteUrl}/${team.invite_code}/`" target="_blank">this URL</a>, to people to allow them to join <span class="has-text-primary">{{ team.name }}</span>!</p>
          </div>
        </div>

        <div class="columns">
          <div class="column is-full">
            <button class="button is-success is-fullwidth" @click="saveDetails">
              <span class="icon-text">
                <span class="icon"><i class="material-icons">save</i></span>
                <span>Save</span>
              </span>
            </button>
          </div>
        </div>

        <div class="columns">
          <div class="column is-half">
            <div class="card">
              <div class="card-header">
                <div class="card-header-title">General</div>
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
                      <option v-for="member in realMembers" :key="member.id" :value="member.character.id">{{ member.name }}</option>
                    </select>
                  </div>
                  <p class="help is-warning">Changing this will lock you out of this page. Please be sure you want to hand over leadership before changing this value.</p>
                  <p v-if="errors.team_lead !== undefined" class="help is-danger">{{ errors.team_lead[0] }}</p>
                </div>
              </div>
              <footer class="card-footer">
                <a class="has-text-danger card-footer-item" @click="disband">
                  <span class="icon-text">
                    <span class="icon"><i class="material-icons">delete</i></span>
                    <span>Disband</span>
                  </span>
                </a>
              </footer>
            </div>
          </div>

          <div class="column is-half">
            <div class="card">
              <div class="card-header">
                <div class="card-header-title">
                  Solver Priority
                </div>
              </div>

              <div class="card-content">
                <div class="table-container">
                  <table class="table">
                    <tr>
                      <td v-for="jobId in teamSolverSortOrder" :key="`solver-${jobId}`">
                        <span class="icon">
                          <img :src="`/job_icons/${jobId}.png`" :alt="`${jobId} job icon`" width="24" height="24" draggable="false" />
                        </span>
                      </td>
                    </tr>
                  </table>
                </div>
                <button class="button is-success is-fullwidth" @click="addOverride">
                  <span class="icon-text">
                    <span class="icon"><i class="material-icons">add</i></span>
                    <span>Add New Override</span>
                  </span>
                </button>
                <br />
                <p v-if="errors.solver_sort_overrides !== undefined" class="has-text-danger">{{ errors.solver_sort_overrides[0] }}</p>
                <template v-for="({ jobId, position }, index) in solverOverrides">
                  <div :key="`override-${index}`" class="box">
                    <div class="field is-horizontal">
                      <div class="field-label is-normal">
                        <label class="label" :for="`override-id-${index}`">Job</label>
                      </div>
                      <div class="field-body">
                        <div class="field">
                          <div class="control has-icons-left">
                            <div class="select" :id="`override-id-${index}`">
                              <select ref="jobPicker" v-model="solverOverrides[index].jobId">
                                <option v-for="job in jobs" :key="job.name" :value="job.id">{{ job.display_name }}</option>
                              </select>
                            </div>
                            <div class="icon is-small is-left">
                              <img :src="`/job_icons/${jobId}.png`" :alt="`${jobId} Job Icon`" width="24" height="24" ref="jobIcon" />
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>

                    <div class="field is-horizontal">
                      <div class="field-label is-normal">
                        <label class="label" :for="`override-position-${index}`">Position</label>
                      </div>
                      <div class="field-body">
                        <div class="field">
                          <div class="control">
                            <input class="input" type="number" :id="`override-position-${index}`" min="1" :max="jobs.length" v-model="solverOverrides[index].position" />
                          </div>
                        </div>
                      </div>
                    </div>

                    <div class="field is-horizontal">
                      <div class="field-label is-normal">
                      </div>
                      <div class="field-body">
                        <div class="field">
                          <div class="control">
                            <button class="button is-danger remove-override" @click="() => removeOverride(index)">
                              <span class="icon-text">
                                <span class="icon"><i class="material-icons">delete</i></span>
                                <span>Remove Override</span>
                              </span>
                            </button>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </template>
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script lang="ts">
import * as Sentry from '@sentry/vue'
import { Component, Vue } from 'vue-property-decorator'
import TeamNav from '@/components/team/nav.vue'
import DeleteTeam from '@/components/modals/confirmations/delete_team.vue'
import { TeamUpdateErrors } from '@/interfaces/responses'
import Team from '@/interfaces/team'
import TeamMember from '@/interfaces/team_member'
import TeamViewMixin from '@/mixins/team_view_mixin'
import Job from '@/interfaces/job'

interface LocalOverride {
  jobId: string
  position: number
}

@Component({
  components: {
    TeamNav,
  },
})
export default class TeamSettings extends TeamViewMixin {
  errors: TeamUpdateErrors = {}

  firstLoad = true

  jobsLoading = true

  solverDefault: string[] = []

  solverOverrides: LocalOverride[] = []

  team!: Team

  teamLeadId!: number

  teamLoading = true

  get inviteUrl(): string {
    return `${process.env.VUE_APP_URL}/team/join`
  }

  get jobs(): Job[] {
    return this.$store.state.jobs
  }

  get loading(): boolean {
    return this.teamLoading || this.jobsLoading
  }

  get realMembers(): TeamMember[] {
    // Return all Members of the Team that aren't Proxies, because Proxies cannot be made lead
    return this.team.members.filter((tm: TeamMember) => !tm.character.proxy)
  }

  get teamSolverSortOrder(): string[] {
    // Combine the default sort order and the overrides to generate the list of Job IDs on the table
    const table: string[] = []
    if (this.solverDefault.length === 0) return table

    for (let i = 0; i < this.solverDefault.length; i += 1) {
      table.push('')
    }

    // Loop through the overrides on the system, replace the empty strings
    this.solverOverrides.forEach(({ jobId, position }) => {
      table[position - 1] = jobId
    })

    // Loop through the defaults in order, if the job isn't in the overrides map then add it to the array
    const nonOverrides = this.solverDefault.filter((jobId: string) => !table.includes(jobId))
    nonOverrides.forEach((jobId: string) => {
      const replaceIndex = table.indexOf('')
      if (replaceIndex === -1) {
        throw new Error('somehow hit a -1 replace index')
      }
      table[replaceIndex] = jobId
    })
    return table
  }

  get url(): string {
    return `/backend/api/team/${this.teamId}/`
  }

  addOverride(): void {
    this.solverOverrides.push({ jobId: 'PLD', position: 1 })
    this.$forceUpdate()
  }

  checkPermissions(displayWarning: boolean): void {
    // Ensure that the person on this page is the team leader and not anybody else
    if (!this.userIsTeamLead) {
      this.$router.push(`/team/${this.$route.params.teamId}/`, () => {
        if (displayWarning) Vue.notify({ text: 'Only the team leader can edit a Team\'s settings.', type: 'is-warning' })
      })
    }
  }

  created(): void {
    this.fetchTeam(false)
    this.loadDefaultSortOrder()
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
        this.teamLoading = false
        this.firstLoad = false

        // Convert the team's solver sort overrides into the list version
        this.solverOverrides = []
        Object.entries(this.team.solver_sort_overrides).forEach(([jobId, position]) => {
          this.solverOverrides.push({ jobId, position })
        })
        this.solverOverrides.sort((overrideA, overrideB) => overrideA.position - overrideB.position)

        if (reload) this.$forceUpdate()
        document.title = `Settings - ${this.team.name} - Savage Aim`
      }
      else {
        super.handleError(response.status)
      }
    }
    catch (e) {
      this.$notify({ text: `Error ${e} when fetching Team.`, type: 'is-danger' })
      Sentry.captureException(e)
    }
  }

  async load(): Promise<void> {
    this.fetchTeam(true)
  }

  async loadDefaultSortOrder(): Promise<void> {
    // Load the job sort data from the API
    try {
      const response = await fetch('/backend/api/job/solver/')
      if (response.ok) {
        // Parse the JSON into a team and save it
        const details = (await response.json()) as Job[]
        this.solverDefault = details.map((job: Job) => job.id)
        console.log(this.teamSolverSortOrder)
      }
      else {
        this.$notify({ text: 'Could not load Jobs for Solver Order; help display will not work.', type: 'is-warning' })
      }
    }
    catch (e) {
      this.$notify({ text: `Error ${e} when fetching Jobs for Solver Order; help display will not work.`, type: 'is-warning' })
      Sentry.captureException(e)
    }
    finally {
      this.jobsLoading = false
    }
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
      Sentry.captureException(e)
    }
  }

  removeOverride(index: number): void {
    this.solverOverrides.splice(index, 1)
  }

  async saveDetails(): Promise<void> {
    this.errors = {}

    const sortOverrides: { [jobId: string]: number } = {}
    this.solverOverrides.forEach(({ jobId, position }) => {
      sortOverrides[jobId] = position
    })

    const updateObj = {
      name: this.team.name,
      tier_id: this.team.tier.id,
      team_lead: this.teamLeadId,
      solver_sort_overrides: sortOverrides,
    }

    console.log(updateObj)

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
      Sentry.captureException(e)
    }
  }
}
</script>

<style lang="scss">
</style>
