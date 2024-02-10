<template>
  <div>
    <form>
      <label class="label" for="lodestoneUrl">Lodestone Character URL</label>
      <div class="field has-addons">
        <div class="control is-expanded">
          <input class="input" id="lodestoneUrl" :class="{'is-danger': errors.length > 0}" type="url" placeholder="https://eu.finalfantasyxiv.com/lodestone/character/xxxxxxxxx/" ref="url" />
        </div>
        <div class="control">
          <button class="button is-success" :class="{'is-loading': apiLoading || xivLoading}" @click="fetchChar">
            <span class="icon"><i class="material-icons">cloud_download</i></span>
            <span>Import</span>
          </button>
        </div>
      </div>
      <p v-for="(error, i) in errors" :key="i" class="help is-danger">{{ error }}</p>
    </form>
  </div>
</template>

<script lang="ts">
import * as Sentry from '@sentry/vue'
import { Component, Prop, Vue } from 'vue-property-decorator'
import { Character } from '@/interfaces/character'
import { CharacterScrapeData, CharacterScrapeError } from '@/interfaces/lodestone'
import SavageAimMixin from '@/mixins/savage_aim_mixin'

@Component
export default class CharacterForm extends SavageAimMixin {
  @Prop()
  apiErrors!: string[]

  @Prop()
  apiLoading!: boolean

  baseUrl = `/backend/api/lodestone`

  char: Character | null = null

  checkErrors: string[] = []

  // Flag for the first half of the form's loading animation
  xivLoading = false

  regex = /https:\/\/[a-z]{2}\.finalfantasyxiv\.com\/lodestone\/character\/([0-9]+)\/?/

  get errors(): string[] {
    return this.apiErrors.concat(this.checkErrors)
  }

  get urlInput(): HTMLInputElement {
    return this.$refs.url as HTMLInputElement
  }

  async fetchChar(e: Event): Promise<void> {
    e.preventDefault()
    // Don't allow multiple runs of this command
    if (this.xivLoading || this.apiLoading) return

    // Run the thing
    this.xivLoading = true
    this.checkErrors = []

    // Start by sending an xivapi request to ensure that the url is valid
    const lodestoneUrl = this.urlInput.value
    const match = this.regex.exec(lodestoneUrl)
    if (match === null) {
      this.checkErrors = ['The given url is invalid. Please make sure to copy a character url and try again.']
      this.xivLoading = false
      return
    }

    // If we're okay here, we can grab the id and use XIVAPI to check that the ID is correct
    const id = match[1]
    const url = `${this.baseUrl}/${id}`
    try {
      const response = await fetch(url, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': Vue.$cookies.get('csrftoken'),
        },
      })

      if (response.ok) {
        // Using the data we retrieve from XIVAPI, then send a create request to the API.
        const json = await response.json() as CharacterScrapeData
        const char = {
          alias: '',
          avatar_url: json.avatar_url,
          id: -1,
          lodestone_id: id,
          name: json.name,
          world: `${json.world} (${json.dc})`,
          user_id: this.$store.state.user.id,
          token: '',
          verified: false,
        }

        // Bubble up the character with an event
        this.$emit('fetched', char)
      }
      else {
        super.handleError(response.status)
        const json = await response.json() as CharacterScrapeError
        this.checkErrors = [json.message]
      }
    }
    catch (err) {
      this.$notify({ text: `Error ${err} when attempting to create Character.`, type: 'is-danger' })
      Sentry.captureException(err)
    }
    finally {
      this.xivLoading = false
    }
  }
}
</script>

<style lang="scss">

</style>
