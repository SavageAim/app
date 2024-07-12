<template>
  <div>
    <div class="breadcrumb">
      <ul>
        <li><router-link to="/team/">Create or Join a Team</router-link></li>
        <li class="is-active"><a>Create a Team</a></li>
      </ul>
    </div>

    <div class="container">
      <div class="card">
        <div class="card-header">
          <div class="card-header-title">Create a Team!</div>
        </div>
        <div class="card-content">
          <div class="field">
            <label class="label" for="name">Team Name</label>
            <div class="control">
              <input class="input" id="name" type="text" v-model="teamName" />
            </div>
          </div>
          <div class="field">
            <label class="label" for="tier">Tier</label>
            <div class="select is-fullwidth" :class="{'is-danger': errors.tier_id !== undefined}">
              <select v-model="tierId" id="tier">
                <option value="-1">Select a Tier</option>
                <option v-for="tier in $store.state.tiers" :key="tier.id" :value="tier.id">{{ tier.name }}</option>
              </select>
            </div>
            <p v-if="errors.tier_id !== undefined" class="help is-danger">{{ errors.tier_id[0] }}</p>
          </div>
          <div class="divider"><i class="material-icons icon">expand_more</i> Team Leader <i class="material-icons icon">expand_more</i></div>
          <TeamMemberForm ref="form" :bis-list-id-errors="errors.bis_list_id" :character-id-errors="errors.character_id" v-if="characters.length && !createFormUsed" />
          <template v-else>
            <p class="no-chars-message">Your account currently has no Characters.</p>
            <p class="no-chars-message">Provide a Lodestone Character URL, and either an <code>Etro.gg</code> or <code>XIVGear.app</code> Gearset URL, and a Character will automatically be made for you!</p>
            <p class="no-chars-message">Otherwise, visit the <a href="/characters/new/" target="_blank">New Character</a> page if you'd like to do the full process yourself!</p>
            <hr />
            <TeamMemberCreateNewCharacterForm ref="characterCreateForm" />
          </template>
        </div>
        <div class="card-footer">
          <p class="card-footer-item is-loading" v-if="requesting || createFormRunning"></p>
          <a class="card-footer-item has-text-success" @click="create" v-else-if="characters.length && !createFormUsed">
            <span class="icon-text">
              <span class="icon"><i class="material-icons">add</i></span>
              Create Team
            </span>
          </a>
          <a class="card-footer-item has-text-success" @click="createCharAndTeam" v-else>
            <span class="icon-text">
              <span class="icon"><i class="material-icons">add</i></span>
              Create Team
            </span>
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import * as Sentry from '@sentry/vue'
import { Component, Vue } from 'vue-property-decorator'
import TeamMemberForm from '@/components/team/member_form.vue'
import TeamMemberCreateNewCharacterForm from '@/components/team/membership_new_character_form.vue'
import { Character } from '@/interfaces/character'
import { TeamCreateErrors, TeamCreateResponse } from '@/interfaces/responses'
import SavageAimMixin from '@/mixins/savage_aim_mixin'
import Tier from '@/interfaces/tier'

@Component({
  components: {
    TeamMemberForm,
    TeamMemberCreateNewCharacterForm,
  },
})
export default class TeamCreate extends SavageAimMixin {
  createFormRunning = false

  createFormUsed = false

  errors: TeamCreateErrors = {}

  requesting = false

  teamName = ''

  tierId = '-1'

  url = `/backend/api/team/`

  // Values for sending
  get bisListId(): string {
    try {
      return (this.$refs.form as TeamMemberForm).bisListId
    }
    catch (e) {
      return `${this.characterCreateForm.bisList?.id || '-1'}`
    }
  }

  get characters(): Character[] {
    return this.$store.state.characters
  }

  get characterCreateForm(): TeamMemberCreateNewCharacterForm {
    return this.$refs.characterCreateForm as TeamMemberCreateNewCharacterForm
  }

  get characterId(): string {
    try {
      return (this.$refs.form as TeamMemberForm).characterId
    }
    catch (e) {
      return `${this.characterCreateForm.character?.id || '-1'}`
    }
  }

  get tier(): Tier | null {
    return this.$store.state.tiers.find((tier: Tier) => tier.id === parseInt(this.tierId, 10)) || null
  }

  mounted(): void {
    document.title = 'Create New Team - Savage Aim'
  }

  async create(): Promise<void> {
    if (this.requesting) return
    this.requesting = true

    const body = JSON.stringify({
      name: this.teamName,
      tier_id: this.tierId,
      bis_list_id: this.bisListId,
      character_id: this.characterId,
    })
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
          Vue.notify({ text: 'Team created successfully!', type: 'is-success' })
        })
      }
      else {
        super.handleError(response.status)
        this.errors = (await response.json() as TeamCreateErrors)
      }
    }
    catch (e) {
      this.$notify({ text: `Error ${e} when attempting to create a Team.`, type: 'is-danger' })
      Sentry.captureException(e)
    }
    finally {
      this.requesting = false
    }
  }

  async createCharAndTeam(): Promise<void> {
    if (this.createFormRunning) return
    this.errors = {}
    if (this.tier === null) {
      this.errors.tier_id = ['Please select a Tier!']
      return
    }
    this.createFormUsed = true
    this.createFormRunning = true
    const created = await this.characterCreateForm.createCharAndBIS(this.tier)
    if (created) await this.create()
    this.createFormRunning = false
  }

  async load(): Promise<void> {
    this.$forceUpdate()
  }
}
</script>

<style lang="scss">
.no-chars-message {
  margin-bottom: 0.25rem;
}
</style>
