<template>
  <div>
    <div class="field is-horizontal">
      <div class="field-label is-normal">
        <label class="label" for="lodestoneUrl">Character</label>
      </div>
      <div class="field-body">
        <div class="field">
          <div class="control is-expanded">
            <input class="input" :class="{'is-danger': characterErrors.length > 0, 'is-success': characterLoaded}" id="lodestoneUrl" type="url" placeholder="https://eu.finalfantasyxiv.com/lodestone/character/xxxxxxxxx/" ref="lodestoneUrl" />
          </div>
          <p v-for="(error, i) in characterErrors" :key="`character-error-${i}`" class="help is-danger">{{ error }}</p>
        </div>
      </div>
    </div>

    <div class="field is-horizontal">
      <div class="field-label is-normal">
        <label class="label" for="etroUrl">Gearset</label>
      </div>
      <div class="field-body">
        <div class="field">
          <div class="control is-expanded">
            <input class="input" :class="{'is-danger': etroErrors.length > 0, 'is-success': etroLoaded}" id="etroUrl" type="url" placeholder="https://etro.gg/gearset/xxxxxxx/" ref="etroUrl" />
          </div>
          <p v-for="(error, i) in etroErrors" :key="`etro-error-${i}`" class="help is-danger">{{ error }}</p>
        </div>
      </div>
    </div>

    <p>If the Job of the Etro Gearset is supported by the gear equipped according to Lodestone, your current gear from Lodestone will be used for the BIS.</p>
    <p>Otherwise, your Current Gear will be set to the Tier's Crafted Set!</p>
  </div>
</template>

<script lang="ts">
import * as Sentry from '@sentry/vue'
import { Component, Vue } from 'vue-property-decorator'
import { CharacterScrapeData, CharacterScrapeError } from '@/interfaces/lodestone'
import Team from '@/interfaces/team'
import Tier from '@/interfaces/tier'
import SavageAimMixin from '@/mixins/savage_aim_mixin'
import { Character } from '@/interfaces/character'
import { CharacterCreateErrors, CreateResponse } from '@/interfaces/responses'

@Component
export default class TeamMemberCreateNewCharacterForm extends SavageAimMixin {
  characterCreateUrl = '/backend/api/character/'

  characterErrors: string[] = []

  characterImportUrl = '/backend/api/lodestone'

  characterLoaded = false

  characterUrlRegex = /https:\/\/[a-z]{2}\.finalfantasyxiv\.com\/lodestone\/character\/([0-9]+)\/?/

  etroErrors: string[] = []

  etroLoaded = false

  get etroUrlField(): HTMLInputElement {
    return this.$refs.etroUrl as HTMLInputElement
  }

  get lodestoneUrlField(): HTMLInputElement {
    return this.$refs.lodestoneUrl as HTMLInputElement
  }

  private async createCharacter(): Promise<number> {
    this.characterErrors = []
    this.characterLoaded = false
    const char = await this.importCharacter()
    if (char === null) return -1

    const body = JSON.stringify(char)
    try {
      const response = await fetch(this.characterCreateUrl, {
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
        return json.id
      }
      super.handleError(response.status)
      const json = await response.json() as CharacterCreateErrors
      if (json.lodestone_id != null) {
        this.characterErrors = json.lodestone_id
      }
      // Catch all error message for anything other than lodestone id
      else if (Object.keys(json).length > 0) {
        this.characterErrors = ['Something went wrong that shouldn\'t have, please inform Eri on the Discord. Sorry for the inconvenience!']
      }
    }
    catch (e) {
      this.$notify({ text: `Error ${e} when attempting to create Character.`, type: 'is-danger' })
      Sentry.captureException(e)
    }
    finally {
      this.characterLoaded = true
    }
    return -1
  }

  public async createTeam(teamName: string, tier: Tier): Promise<void> {
    const charId = await this.createCharacter()
    if (charId === -1) return
    // TODO - Make BIS stuff
  }

  private async importCharacter(): Promise<Character | null> {
    // Start by sending an xivapi request to ensure that the url is valid
    const lodestoneUrl = this.lodestoneUrlField.value
    const match = this.characterUrlRegex.exec(lodestoneUrl)
    if (match === null) {
      this.characterErrors = ['The given url is invalid. Please make sure to copy a character url and try again.']
      return null
    }

    // If we're okay here, we can grab the id and use XIVAPI to check that the ID is correct
    const id = match[1]
    const url = `${this.characterImportUrl}/${id}`
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
          proxy: false,
          bis_lists: [],
        }

        // Bubble up the character with an event
        return char
      }
      super.handleError(response.status)
      const json = await response.json() as CharacterScrapeError
      this.characterErrors = [json.message]
    }
    catch (err) {
      this.$notify({ text: `Error ${err} when attempting to create Character.`, type: 'is-danger' })
      Sentry.captureException(err)
    }
    return null
  }

  public async joinTeam(team: Team): Promise<void> {
    const charId = await this.createCharacter()
    if (charId === -1) return
  }
}
</script>

<style lang="scss">
</style>
