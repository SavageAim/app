<template>
  <div>
    <div class="card-header">
      <div class="card-header-title">
        Are you sure you want to delete the following character?
      </div>
      <div class="card-header-icon">
        <a @click="() => { this.$emit('close') }" class="icon">
          <i class="material-icons">close</i>
        </a>
      </div>
    </div>
    <div class="card-content">
      <CharacterBio :character="character" :displayUnverified="false" />
    </div>
    <div class="card-footer">
      <a class="card-footer-item" @click="() => { this.$emit('close') }">Cancel</a>
      <a class="card-footer-item has-text-danger" @click="deleteCharacter">Delete</a>
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
