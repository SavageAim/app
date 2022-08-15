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
          <TeamMemberForm ref="form" :bis-list-id-errors="errors.bis_list_id" :character-id-errors="errors.character_id" v-if="characters.length" />
          <template v-else>
            <p class="no-chars-message">Your account currently has no Characters.</p>
            <p class="no-chars-message">Clicking the "Add Character" button below will open the page to add a new Character to your account in another tab.</p>
            <p class="no-chars-message">When your Character has been imported and verified this page will automatically update with them to allow you to select them to be your Team Leader Character!</p>
            <a href="/characters/new/" target="_blank" class="button is-success is-fullwidth">
              <span class="icon-text">
                <span class="icon"><i class="material-icons">open_in_new</i></span>
                <span>Add Character</span>
              </span>
            </a>
          </template>
        </div>
        <div class="card-footer">
          <a class="card-footer-item has-text-success" @click="create">Create Team</a>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import TeamMemberForm from '@/components/team/member_form.vue'
import { Character } from '@/interfaces/character'
import { TeamCreateErrors, TeamCreateResponse } from '@/interfaces/responses'
import SavageAimMixin from '@/mixins/savage_aim_mixin'

@Component({
  components: {
    TeamMemberForm,
  },
})
export default class TeamJoin extends SavageAimMixin {
  errors: TeamCreateErrors = {}

  teamName = ''

  tierId = '-1'

  url = `/backend/api/team/`

  // Values for sending
  get bisListId(): string {
    return (this.$refs.form as TeamMemberForm).bisListId
  }

  get characters(): Character[] {
    return this.$store.state.characters
  }

  get characterId(): string {
    return (this.$refs.form as TeamMemberForm).characterId
  }

  mounted(): void {
    document.title = 'Create New Team - Savage Aim'
  }

  async create(): Promise<void> {
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
    }
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
