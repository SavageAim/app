<template>
  <div>
    <div class="card-header">
      <div class="card-header-title">Do you wish to attempt to claim this Character?</div>
      <div class="card-header-icon">
        <a @click="() => { this.$emit('close') }" class="icon">
          <i class="material-icons">close</i>
        </a>
      </div>
    </div>
    <div class="card-content">
      <div class="box">
        <CharacterBio :character="details" :displayUnverified="false" />
      </div>
    </div>
    <div class="card-footer">
      <a class="card-footer-item" @click="() => { this.$emit('close') }">Cancel</a>
      <a class="card-footer-item has-text-success" @click="claimCharacter">Claim Character</a>
    </div>
  </div>
</template>

<script lang="ts">
import * as Sentry from '@sentry/vue'
import { Component, Prop, Vue } from 'vue-property-decorator'
import CharacterBio from '@/components/character_bio.vue'
import { Character } from '@/interfaces/character'
import { CreateResponse } from '@/interfaces/responses'

@Component({
  components: {
    CharacterBio,
  },
})
export default class ClaimCharacter extends Vue {
  @Prop()
  code!: string

  @Prop()
  details!: Character

  @Prop()
  teamId!: number

  get url(): string {
    return `/backend/api/team/${this.teamId}/proxies/${this.details.id}/claim/`
  }

  async claimCharacter(): Promise<void> {
    try {
      const response = await fetch(this.url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': Vue.$cookies.get('csrftoken'),
        },
        body: JSON.stringify({ invite_code: this.code }),
      })

      if (response.ok) {
        // Attempt to parse the json, get the id, and then redirect
        const json = await response.json() as CreateResponse
        this.$store.dispatch('fetchCharacters')
        this.$emit('close')
        // Move to the new Character page
        this.$router.push(`/characters/${json.id}/`, () => {
          Vue.notify({ text: `Please follow the verification instructions to finish claiming this Character.`, type: 'is-success' })
        })
      }
      else {
        this.$notify({ text: `Unexpected response ${response.status} when attempting to claim Character.`, type: 'is-danger' })
      }
    }
    catch (e) {
      this.$notify({ text: `Error ${e} when attempting to claim Character.`, type: 'is-danger' })
      Sentry.captureException(e)
    }
  }
}
</script>
