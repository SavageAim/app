<template>
  <div id="new-char" class="container">
    <div class="card">
      <div class="card-header">
        <div class="card-header-title">
          <h2 class="title">Add A Character</h2>
        </div>
      </div>
      <div class="card-content">
        <p>Paste the Lodestone URL into the box below and hit Import to import your character.</p>
        <p>After importing, there will be a necessary verification step before you can start making lists and/or teams.</p>
        <hr />
        <CharacterForm :api-errors="errors" :api-loading="loading" @fetched="sendCharacter" />
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import CharacterForm from '@/components/character_form.vue'
import { Character } from '@/interfaces/character'
import { CreateResponse, CharacterCreateErrors } from '@/interfaces/responses'
import SavageAimMixin from '@/mixins/savage_aim_mixin'

@Component({
  components: {
    CharacterForm,
  },
})
export default class NewChar extends SavageAimMixin {
  errors: string[] = []

  loading = false

  url = `/backend/api/character/`

  get urlInput(): HTMLInputElement {
    return this.$refs.url as HTMLInputElement
  }

  mounted(): void {
    document.title = 'Add New Character - Savage Aim'
  }

  async sendCharacter(char: Character): Promise<void> {
    // Function that is solely for handling interacting with the savageaim api
    // No need for try / catch since it's called inside a try catch block already
    this.loading = true
    const body = JSON.stringify(char)
    try {
      const response = await fetch(this.url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': Vue.$cookies.get('csrftoken'),
        },
        body,
      })

      if (response.ok) {
        // Attempt to parse the json, get the id, and then redirect
        const json = await response.json() as CreateResponse
        this.$store.dispatch('fetchCharacters')
        this.$router.push(`/characters/${json.id}/`, () => {
          Vue.notify({ text: `New Character created successfully!`, type: 'is-success' })
        })
      }
      else {
        super.handleError(response.status)
        const json = await response.json() as CharacterCreateErrors
        if (json.lodestone_id != null) {
          this.errors = json.lodestone_id
        }
        // Catch all error message for anything other than lodestone id
        else if (Object.keys(json).length > 0) {
          this.errors = ['Something went wrong that shouldn\'t have, please inform Eri on the Discord. Sorry for the inconvenience!']
        }
      }
    }
    catch (e) {
      this.$notify({ text: `Error ${e} when attempting to create Character.`, type: 'is-danger' })
    }
    finally {
      this.loading = false
    }
  }
}
</script>

<style lang="scss">

</style>
