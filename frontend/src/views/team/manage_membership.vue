<template>
  <div>
    <div v-if="!loaded">
      <button class="button is-static is-loading is-fullwidth">Loading</button>
    </div>

    <template v-else>
      <div class="breadcrumb">
        <ul>
          <li><router-link :to="`/team/${team.id}/`">{{ team.name }}</router-link></li>
          <li class="is-active"><a>Update Membership</a></li>
        </ul>
      </div>

      <div class="container">
        <div class="card">
          <div class="card-header">
            <div class="card-header-title">Update Membership in {{ team.name }}</div>
          </div>
          <div class="card-content">
            <p>Below you can change which of your Characters are in the Team, and/or the BIS List they will be using.</p>
            <hr />
            <TeamMemberForm ref="form" :bis-list-id-errors="errors.bis_list_id" :character-id-errors="errors.character_id" :initial-character-id="member.character.id" :initial-bis-list-id="member.bis_list.id" />
          </div>
          <div class="card-footer">
            <a class="card-footer-item has-text-success" @click="save">
              <span class="icon-text">
                <span class="icon"><i class="material-icons">save</i></span>
                <span>Save</span>
              </span>
            </a>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script lang="ts">
import * as Sentry from '@sentry/vue'
import { Component, Prop } from 'vue-property-decorator'
import TeamMemberForm from '@/components/team/member_form.vue'
import { TeamMemberUpdateErrors } from '@/interfaces/responses'
import Team from '@/interfaces/team'
import TeamMember from '@/interfaces/team_member'
import SavageAimMixin from '@/mixins/savage_aim_mixin'

@Component({
  components: {
    TeamMemberForm,
  },
})
export default class TeamManageMembership extends SavageAimMixin {
  memberLoaded = false

  teamLoaded = false

  errors: TeamMemberUpdateErrors = {}

  member!: TeamMember

  @Prop()
  memberId!: string

  team!: Team

  @Prop()
  teamId!: string

  // Values for sending
  get bisListId(): string {
    return (this.$refs.form as TeamMemberForm).bisListId
  }

  get characterId(): string {
    return (this.$refs.form as TeamMemberForm).characterId
  }

  get loaded(): boolean {
    return this.memberLoaded && this.teamLoaded
  }

  get teamUrl(): string {
    return `/backend/api/team/${this.teamId}/`
  }

  get url(): string {
    return `${this.teamUrl}member/${this.memberId}/`
  }

  created(): void {
    this.fetchTeam()
    this.fetchMember()
  }

  async fetchMember(): Promise<void> {
    // Load the member data from the API
    try {
      const response = await fetch(this.url)
      if (response.ok) {
        // Parse the JSON into a team and save it
        this.member = (await response.json()) as TeamMember
        this.memberLoaded = true
      }
      else {
        super.handleError(response.status)
      }
    }
    catch (e) {
      this.$notify({ text: `Error ${e} when fetching Team Member.`, type: 'is-danger' })
      Sentry.captureException(e)
    }
  }

  async fetchTeam(): Promise<void> {
    // Load the team data from the API
    try {
      const response = await fetch(this.teamUrl)
      if (response.ok) {
        // Parse the JSON into a team and save it
        this.team = (await response.json()) as Team
        this.teamLoaded = true
        document.title = `Manage Membership - ${this.team.name} - Savage Aim`
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

  async save(): Promise<void> {
    this.errors = {}

    const body = JSON.stringify({ bis_list_id: this.bisListId, character_id: this.characterId })
    try {
      const response = await fetch(this.url, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': this.$cookies.get('csrftoken'),
        },
        body,
      })

      if (response.ok) {
        // Just display a message and force an update
        this.$notify({ text: 'Successfully updated!', type: 'is-success' })
        this.$forceUpdate()
      }
      else {
        super.handleError(response.status)
        this.errors = (await response.json() as TeamMemberUpdateErrors)
      }
    }
    catch (e) {
      this.$notify({ text: `Error ${e} when attempting to create BIS List.`, type: 'is-danger' })
      Sentry.captureException(e)
    }
  }
}
</script>

<style lang="scss">
</style>
