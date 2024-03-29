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
            <p v-for="(error, i) in characterApiErrors" :key="i" class="help is-danger">{{ error }}</p>
          </template>
        </div>
        <div class="card-footer" v-if="character !== null">
          <a class="card-footer-item has-text-success" @click="createProxy">
            <span class="icon-text">
              <span class="icon"><i class="material-icons">add</i></span>
              <span>Create Proxy</span>
            </span>
          </a>
          <a class="card-footer-item" @click="changeCharacter">
            <span class="icon-text">
              <span class="icon"><i class="material-icons">cloud_sync</i></span>
              <span>Change Character</span>
            </span>
          </a>
        </div>
      </div>

      <BISListForm :bisList="bis" :external-errors="bisApiErrors" :character="character" :url="''" method="" :char-is-proxy="true" />
    </template>
  </div>
</template>

<script lang="ts">
import * as Sentry from '@sentry/vue'
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

  changeCharacter(): void {
    this.character = null
    this.characterApiErrors = []
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
      Sentry.captureException(e)
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
      Sentry.captureException(e)
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
