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
          <li class="is-active"><a aria-current="page">New</a></li>
        </ul>
      </div>

      <div class="card">
        <div class="card-content">
          <CharacterForm :api-errors="characterApiErrors" :api-loading="requesting" @fetched="updateChar" v-if="character === null" />
          <template v-else>
            <div class="box" id="char-box">
              <CharacterBio :character="character" :displayUnverified="false" />
            </div>
            <div class="field has-addons">
              <div class="control is-expanded">
                <button class="button is-danger is-fullwidth" @click="() => { this.character = null }">Change Character</button>
              </div>
              <div class="control is-expanded">
                <button class="button is-success is-fullwidth" @click="createProxy">Create Proxy</button>
              </div>
            </div>
          </template>
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
import CharacterForm from '@/components/character_form.vue'
import BISListModify from '@/dataclasses/bis_list_modify'
import { Character } from '@/interfaces/character'
import Team from '@/interfaces/team'
import {
  BISListErrors,
  ProxyCreateErrors,
} from '@/interfaces/responses'
import TeamViewMixin from '@/mixins/team_view_mixin'

@Component({
  components: {
    BISListForm,
    CharacterBio,
    CharacterForm,
  },
})
export default class NewProxy extends TeamViewMixin {
  bis = new BISListModify()

  bisApiErrors: BISListErrors = {}

  character: Character | null = null

  // This just comes from response.lodestone_id
  characterApiErrors: string[] = []

  loading = true

  requesting = false

  team!: Team

  get readUrl(): string {
    return `/backend/api/team/${this.teamId}/`
  }

  get writeUrl(): string {
    return `/backend/api/team/${this.teamId}/proxies/`
  }

  checkPermissions(): void {
    // Ensure that the person on this page is the team leader and not anybody else
    if (!this.userHasProxyManagerPermission) {
      this.$router.push(`/team/${this.team.id}/`, () => {
        Vue.notify({ text: 'You do not have permission to manage Proxy Characters.', type: 'is-warning' })
      })
    }
  }

  created(): void {
    this.fetchTeam(false)
  }

  updateChar(char: Character): void {
    this.character = char
  }

  // API Interaction
  async createProxy(): Promise<void> {
    // Don't allow multiple requests
    if (this.character === null || this.requesting) return
    this.requesting = true

    const body = JSON.stringify({ character: this.character, bis: this.bis })
    try {
      const response = await fetch(this.writeUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': Vue.$cookies.get('csrftoken'),
        },
        body,
      })

      if (response.ok) {
        // Redirect back to Team Details
        this.$store.dispatch('fetchCharacters')
        this.$router.push(`/team/${this.team.id}/management/`, () => {
          Vue.notify({ text: `New Proxy Character created successfully!`, type: 'is-success' })
        })
      }
      else {
        super.handleError(response.status)
        const json = await response.json() as ProxyCreateErrors
        if (json.character.lodestone_id != null) {
          this.characterApiErrors = json.character.lodestone_id
        }
        this.bisApiErrors = json.bis
      }
    }
    catch (e) {
      this.$notify({ text: `Error ${e} when attempting to create proxy Character.`, type: 'is-danger' })
    }
    finally {
      this.requesting = false
    }
  }

  async fetchTeam(reload: boolean): Promise<void> {
    // Load the team data from the API
    try {
      const response = await fetch(this.readUrl)
      if (response.ok) {
        // Parse the JSON into a team and save it
        this.team = (await response.json()) as Team
        this.checkPermissions()
        this.loading = false
        if (reload) this.$forceUpdate()
        document.title = `New Proxy - ${this.team.name} - Savage Aim`
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
#char-box {
  margin-bottom: 0;
}
</style>
