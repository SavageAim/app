<template>
  <div>
    <div class="card-header">
      <div class="card-header-title"></div>
      <div class="card-header-icon">
        <a @click="() => { this.$emit('close') }" class="icon">
          <i class="material-icons">close</i>
        </a>
      </div>
    </div>
    <div class="card-content">
      <h2 class="subtitle">Are you sure you want to delete this Character?</h2>
      <hr />
      <CharacterBio :character="character" :displayUnverified="false" />
      <hr />
      <h2 class="subtitle">Results of Deletion</h2>
      <div v-if="!character.verified">
        Character isn't verified, so it is safe to delete!
      </div>
      <div v-else-if="loading">
        <button class="button is-static is-loading is-fullwidth">Loading</button>
      </div>
      <div class="content" v-else>
        <ul>
          <template v-for="team in details">
            <li v-if="team.members === 1" :key="team.name"><b>{{ team.name }}</b> will be disbanded.</li>
            <li v-else-if="team.lead" :key="team.name">Team Leadership of <b>{{ team.name }}</b> will be given to another Character, and this Character will leave the Team.</li>
            <li v-else :key="team.name">This Character will leave <b>{{ team.name }}</b>.</li>
          </template>
          <li>All BIS Lists belonging to this character will be deleted.</li>
        </ul>
      </div>
      <hr />
      <p>Please type <code>{{ deleteCheck }}</code> to confirm.</p>
      <input class="input" v-model="input" />
    </div>
    <div class="card-footer">
      <a class="card-footer-item" @click="() => { this.$emit('close') }">Cancel</a>
      <a class="card-footer-item has-text-danger" v-if="canDelete" @click="deleteCharacter">Delete</a>
      <p class="card-footer-item disabled-delete" v-else data-microtip-position="top" role="tooltip" aria-label="Please confirm deletion.">Delete</p>
    </div>
  </div>
</template>

<script lang="ts">
import * as Sentry from '@sentry/vue'
import { Component, Prop, Vue } from 'vue-property-decorator'
import CharacterBio from '@/components/character_bio.vue'
import { CharacterDetails } from '@/interfaces/character'
import { CharacterDeleteReadResponse } from '@/interfaces/responses'

@Component({
  components: {
    CharacterBio,
  },
})
export default class DeleteCharacter extends Vue {
  @Prop()
  character!: CharacterDetails

  details: CharacterDeleteReadResponse[] = []

  input = ''

  loading = true

  get canDelete(): boolean {
    return this.input === this.deleteCheck
  }

  get deleteCheck(): string {
    return `${this.character.name} @ ${this.character.world.split(' ')[0]}`
  }

  get url(): string {
    return `/backend/api/character/${this.character.id}/delete/`
  }

  mounted(): void {
    if (this.character.verified) this.getDeleteInfo()
  }

  async getDeleteInfo(): Promise<void> {
    // Load the character data from the API
    try {
      const response = await fetch(this.url)
      if (response.ok) {
        // Parse the list into an array of character interfaces and store them in the character data list
        this.details = (await response.json()) as CharacterDeleteReadResponse[]
        this.loading = false
      }
      else {
        this.$notify({ text: `Unexpected HTTP Error ${response.status} when fetching Character deletion results.`, type: 'is-danger' })
      }
    }
    catch (e) {
      this.$notify({ text: `Error ${e} when fetching Character deletion results.`, type: 'is-danger' })
      Sentry.captureException(e)
    }
  }

  async deleteCharacter(): Promise<void> {
    try {
      const response = await fetch(this.url, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': Vue.$cookies.get('csrftoken'),
        },
      })

      if (response.ok) {
        // Attempt to parse the json, get the id, and then redirect
        this.$store.dispatch('fetchCharacters')
        this.$emit('close')
        this.$router.push('/', () => {
          Vue.notify({ text: `${this.character.name} (${this.character.world}) deleted successfully!`, type: 'is-success' })
        })
      }
      else {
        this.$notify({ text: `Unexpected response ${response.status} when attempting to delete ${this.character.name}.`, type: 'is-danger' })
      }
    }
    catch (e) {
      this.$notify({ text: `Error ${e} when attempting to delete ${this.character.name}.`, type: 'is-danger' })
      Sentry.captureException(e)
    }
  }
}
</script>
