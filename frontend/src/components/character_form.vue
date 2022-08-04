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
            Import
          </button>
        </div>
      </div>
      <p v-for="(error, i) in errors" :key="i" class="help is-danger">{{ error }}</p>
    </form>
  </div>
</template>

<script lang="ts">
import { Component, Prop } from 'vue-property-decorator'
import XIVAPI from '@xivapi/js'
import { Character } from '@/interfaces/character'
import SavageAimMixin from '@/mixins/savage_aim_mixin'

@Component
export default class CharacterForm extends SavageAimMixin {
  @Prop()
  apiErrors!: string[]

  @Prop()
  apiLoading!: boolean

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
    const xiv = new XIVAPI()
    try {
      const response = await xiv.character.get(id)

      // Using the data we retrieve from XIVAPI, then send a create request to the API.
      const char = {
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

      // Bubble up the character with an event
      this.$emit('fetched', char)
    }
    catch (err) {
      if (err.error != null) {
        // XIVAPI Error
        this.checkErrors = [err.error.Message]
      }
      else {
        // Normal JS error
        this.checkErrors = [err.message]
      }
    }
    finally {
      this.xivLoading = false
    }
  }
}
</script>

<style lang="scss">

</style>
