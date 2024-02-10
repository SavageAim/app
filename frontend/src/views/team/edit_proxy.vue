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
        </div>
        <div class="card-footer" v-if="character !== null">
          <a class="card-footer-item has-text-success" @click="save">
            <span class="icon-text">
              <span class="icon"><i class="material-icons">save</i></span>
              <span>Save Proxy</span>
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
import { Component, Prop, Vue } from 'vue-property-decorator'
import BISListForm from '@/components/bis_list/form.vue'
import CharacterBio from '@/components/character_bio.vue'
import BISListModify from '@/dataclasses/bis_list_modify'
import { Character } from '@/interfaces/character'
import Team from '@/interfaces/team'
import TeamMember from '@/interfaces/team_member'
import { BISListErrors } from '@/interfaces/responses'
import TeamViewMixin from '@/mixins/team_view_mixin'

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
export default class EditProxy extends TeamViewMixin {
  // Need this to be declared as a new one *first* before the load
  // Or else watchers cannot set up correctly
  bis: BISListModify = new BISListModify()

  bisApiErrors: BISListErrors = {}

  character!: Character

  @Prop()
  charId!: string

  loading = true

  requesting = false

  team!: Team

  get url(): string {
    return `/backend/api/team/${this.teamId}/proxies/${this.charId}/`
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
        this.$router.push(`/team/${this.team.id}/management/`, () => {
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
      Sentry.captureException(e)
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
      Sentry.captureException(e)
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
