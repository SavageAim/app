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
      <h2 class="subtitle">Are you sure you want to delete the following character?</h2>
      <hr />
      <CharacterBio :character="character" :displayUnverified="false" />
      <hr />
      <h2 class="subtitle">Results of Deletion</h2>
      <div class="content">
        <!-- TODO - Populate this part with API info -->
        <ul>
          <li>Team Leadership of <b>Hi Wiki!</b> will be handed over to another character, and will be left.</li>
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
import { Component, Prop, Vue } from 'vue-property-decorator'
import CharacterBio from '@/components/character_bio.vue'
import { CharacterDetails } from '@/interfaces/character'

@Component({
  components: {
    CharacterBio,
  },
})
export default class DeleteCharacter extends Vue {
  @Prop()
  character!: CharacterDetails

  input = ''

  get canDelete(): boolean {
    return this.input === this.deleteCheck
  }

  get deleteCheck(): string {
    return `${this.character.name} @ ${this.character.world.split(' ')[0]}`
  }

  get url(): string {
    return `/backend/api/character/${this.character.id}/`
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
    }
  }
}
</script>
