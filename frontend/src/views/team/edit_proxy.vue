<template>
  <div>
    <div v-if="loading">
      <button class="button is-static is-loading is-fullwidth">Loading</button>
    </div>

    <template v-else>
      <div class="breadcrumb">
        <ul>
          <li><router-link :to="`/team/${team.id}/`">{{ team.name }}</router-link></li>
          <li class="is-active"><a href="#">Proxy Characters</a></li>
          <li class="is-active"><a aria-current="page">{{ character.name }}</a></li>
        </ul>
      </div>

      <div class="card">
        <div class="card-content">
          <div class="box" id="char-box">
            <CharacterBio :character="character" :displayUnverified="false" />
          </div>
          <div class="field has-addons">
            <div class="control is-expanded">
              <button class="button is-success is-fullwidth" @click="save">Update BIS</button>
            </div>
          </div>
        </div>
      </div>

      <BISListForm :bisList="bis" :external-errors="bisApiErrors" :character="character" :url="''" method="" :char-is-proxy="true" />
    </template>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import BISListForm from '@/components/bis_list/form.vue'
import CharacterBio from '@/components/character_bio.vue'
import BISListModify from '@/dataclasses/bis_list_modify'
import { Character } from '@/interfaces/character'
import Team from '@/interfaces/team'
import TeamMember from '@/interfaces/team_member'
import { BISListErrors } from '@/interfaces/responses'
import SavageAimMixin from '@/mixins/savage_aim_mixin'

interface ReadResponse {
  team: Team
  member: TeamMember
}

@Component({
  components: {
    BISListForm,
    CharacterBio,
  },
})
export default class NewProxy extends SavageAimMixin {
  bis!: BISListModify

  bisApiErrors: BISListErrors = {}

  character!: Character

  loading = true

  requesting = false

  team!: Team

  // Flag stating whether the currently logged user can edit the Team
  get editable(): boolean {
    return this.team.members.find((teamMember: TeamMember) => teamMember.character.user_id === this.$store.state.user.id)?.lead ?? false
  }

  get url(): string {
    return `/backend/api/team/${this.$route.params.teamId}/proxies/${this.$route.params.id}/`
  }

  checkPermissions(): void {
    // Ensure that the person on this page is the team leader and not anybody else
    if (!this.editable) {
      this.$router.push(`/team/${this.team.id}/`, () => {
        Vue.notify({ text: 'Only the team leader can manage proxies.', type: 'is-warning' })
      })
    }
  }

  created(): void {
    this.fetchProxy(false)
  }

  // API Interaction
  async save(): Promise<void> {
    // Don't allow multiple requests
    if (this.requesting) return
    this.requesting = true

    const body = JSON.stringify(this.bis)
    try {
      const response = await fetch(this.url, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': Vue.$cookies.get('csrftoken'),
        },
        body,
      })

      if (response.ok) {
        // Attempt to parse the json, get the id, and then redirect
        this.$store.dispatch('fetchCharacters')
        this.$router.push(`/team/${this.team.id}/`, () => {
          Vue.notify({ text: `Proxy Character ${this.character.name} updated successfully!`, type: 'is-success' })
        })
      }
      else {
        super.handleError(response.status)
        // Only Errors are BISList errors
        this.bisApiErrors = await response.json() as BISListErrors
      }
    }
    catch (e) {
      this.$notify({ text: `Error ${e} when attempting to update Proxy Character.`, type: 'is-danger' })
    }
    finally {
      this.requesting = false
    }
  }

  async fetchProxy(reload: boolean): Promise<void> {
    // Load the team data from the API
    try {
      const response = await fetch(this.url)
      if (response.ok) {
        // Parse the JSON into a team and save it
        const json = (await response.json()) as ReadResponse
        this.team = json.team
        this.character = json.member.character
        this.bis = BISListModify.buildEditVersion(json.member.bis_list)
        this.checkPermissions()
        this.loading = false
        if (reload) this.$forceUpdate()
        document.title = `Edit ${this.character.name} - ${this.team.name} - Savage Aim`
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
    this.fetchProxy(true)
  }
}
</script>

<style lang="scss">
#char-box {
  margin-bottom: 0;
}
</style>
