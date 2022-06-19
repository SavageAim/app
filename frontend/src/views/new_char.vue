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
        <form @submit="submitChar">
          <div class="field">
            <label class="label">Lodestone Character URL</label>
            <div class="control">
              <input class="input" :class="{'is-danger': errors.length > 0}" type="url" placeholder="https://eu.finalfantasyxiv.com/lodestone/character/xxxxxxxxx/" ref="url" />
            </div>
            <p v-for="(error, i) in errors" :key="i" class="help is-danger">{{ error }}</p>
          </div>

          <div class="buttons is-right">
            <button class="button is-primary" :class="{'is-loading': loading}">Import</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import XIVAPI from '@xivapi/js'
import { Character } from '@/interfaces/character'
import { CreateResponse, CharacterCreateErrors } from '@/interfaces/responses'
import SavageAimMixin from '@/mixins/savage_aim_mixin'

@Component
export default class NewChar extends SavageAimMixin {
  errors: string[] = []

  loading = false

  regex = /https:\/\/[a-z]{2}\.finalfantasyxiv\.com\/lodestone\/character\/([0-9]+)\/?/

  url = `/backend/api/character/`

  get urlInput(): HTMLInputElement {
    return this.$refs.url as HTMLInputElement
  }

  mounted(): void {
    document.title = 'Add New Character - Savage Aim'
  }

  async submitChar(e: Event): Promise<void> {
    e.preventDefault()
    // Don't allow multiple runs of this command
    if (this.loading) return

    // Run the thing
    this.loading = true
    this.errors = []

    // Start by sending an xivapi request to ensure that the url is valid
    const lodestoneUrl = this.urlInput.value
    const match = this.regex.exec(lodestoneUrl)
    if (match === null) {
      this.errors = ['The given url is invalid. Please make sure to copy a character url and try again.']
      this.loading = false
      return
    }

    // If we're okay here, we can grab the id and use XIVAPI to check that the ID is correct
    const id = match[1]
    const xiv = new XIVAPI()
    try {
      const response = await xiv.character.get(id)

      // Using the data we retrieve from XIVAPI, then send a create request to the API.
      const character = {
        alias: '',
        avatar_url: response.Character.Avatar,
        id: -1,
        lodestone_id: response.Character.ID,
        name: response.Character.Name,
        world: `${response.Character.Server} (${response.Character.DC})`,
        user_id: this.$store.state.user.id,
        token: '',
        verified: false,
      }

      // Stringify this, attempt to send it and handle correct or incorrect responses as necessary
      await this.sendCharacter(character)
    }
    catch (err) {
      if (err.error != null) {
        // XIVAPI Error
        this.errors = [err.error.Message]
      }
      else {
        // Normal JS error
        this.errors = [err.message]
      }
    }
    finally {
      this.loading = false
    }
  }

  async sendCharacter(char: Character): Promise<void> {
    // Function that is solely for handling interacting with the savageaim api
    // No need for try / catch since it's called inside a try catch block already
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
  }
}
</script>

<style lang="scss">

</style>
