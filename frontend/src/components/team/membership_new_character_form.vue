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
        <label class="label" for="bisUrl">Gearset</label>
      </div>
      <div class="field-body">
        <div class="field">
          <div class="control is-expanded">
            <input class="input" :class="{'is-danger': bisUrlErrors.length > 0, 'is-success': bisLoaded}" id="bisUrl" type="url" placeholder="https://etro.gg/gearset/xxxxxxx/ | https://xivgear.app/?page=sl|xxxxxxxxxx" ref="bisUrl" />
          </div>
          <p v-for="(error, i) in bisUrlErrors" :key="`etro-error-${i}`" class="help is-danger">{{ error }}</p>
        </div>
      </div>
    </div>

    <p>If the Job of the BIS Gearset matches your current Lodestone details, then your Current Gear will be imported from there.</p>
    <p>Otherwise, your Current Gear will be set to the Tier's Crafted Set!</p>
  </div>
</template>

<script lang="ts">
import * as Sentry from '@sentry/vue'
import { Component, Vue } from 'vue-property-decorator'
import { CharacterScrapeData, CharacterScrapeError } from '@/interfaces/lodestone'
import Tier from '@/interfaces/tier'
import SavageAimMixin from '@/mixins/savage_aim_mixin'
import { Character } from '@/interfaces/character'
import { CharacterCreateErrors, CreateResponse } from '@/interfaces/responses'
import { ExternalBISGearImportResponse, ImportError, LodestoneImportResponse } from '@/interfaces/imports'
import BISListModify from '@/dataclasses/bis_list_modify'
import Gear from '@/interfaces/gear'

@Component
export default class TeamMemberCreateNewCharacterForm extends SavageAimMixin {
  bisList: BISListModify | null = null

  character: Character | null = null

  characterCreateUrl = '/backend/api/character/'

  characterErrors: string[] = []

  characterImportUrl = '/backend/api/lodestone'

  characterLoaded = false

  characterUrlRegex = /https:\/\/[a-z]{2}\.finalfantasyxiv\.com\/lodestone\/character\/([0-9]+)\/?/

  bisUrlErrors: string[] = []

  bisLoaded = false

  etroUrlRegex = /https:\/\/etro\.gg\/gearset\/([-a-z0-9]+)\/?/

  xivGearUrlRegex = /https:\/\/xivgear.app\/\?page=sl\|([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/

  get bisUrlField(): HTMLInputElement {
    return this.$refs.bisUrl as HTMLInputElement
  }

  bisUrl(): string {
    const url = this.bisUrlField.value
    try {
      const decodedUrl = decodeURI(url)
      if (decodedUrl !== url) this.bisUrlField.value = decodedUrl
      return decodedUrl
    }
    catch (e: unknown) {
      console.log('invalid url')
    }
    return url
  }

  get lodestoneUrlField(): HTMLInputElement {
    return this.$refs.lodestoneUrl as HTMLInputElement
  }

  private checkFieldsHaveValidURLs(): boolean {
    this.characterErrors = []
    this.characterLoaded = false
    this.bisUrlErrors = []
    this.bisLoaded = false

    // Ensure both fields are filled correctly, return true if errors are found, false otherwise
    const lodestoneUrl = this.lodestoneUrlField.value
    const match = this.characterUrlRegex.exec(lodestoneUrl)
    if (match === null) {
      this.characterErrors = ['Please provide a valid Lodestone Character URL!']
    }

    const bisUrl = this.bisUrl()
    const etroMatch = this.etroUrlRegex.exec(bisUrl)
    const xivGearMatch = this.xivGearUrlRegex.exec(bisUrl)
    if (etroMatch === null && xivGearMatch === null) {
      this.bisUrlErrors = ['Please provide a valid Etro.gg/XIVGear.app Gearset URL!']
    }

    return (this.characterErrors.length > 0) || (this.bisUrlErrors.length > 0)
  }

  private async createBIS(tier: Tier): Promise<BISListModify | null> {
    const bisList = new BISListModify()
    // Import BIS Data
    const bisData = await this.importBISGear()
    if (bisData === null) return null

    // Import or Generate Current Data
    const currentData = await this.importCurrentGear(bisData.job_id, tier)
    if (currentData === null) return null

    // Compile, create, and return BIS
    bisList.importBIS(bisData)
    bisList.importCurrentLodestoneGear(currentData)

    const body = JSON.stringify(bisList)
    const charId = this.character?.id || ''
    const url = `/backend/api/character/${charId}/bis_lists/`
    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': this.$cookies.get('csrftoken'),
        },
        body,
      })

      if (response.ok) {
        const json = await response.json() as CreateResponse
        bisList.id = json.id
        return bisList
      }
      this.bisUrlErrors = ['Something went wrong creating your BIS List.']
    }
    catch (e) {
      this.$notify({ text: `Error ${e} when attempting to create BIS List.`, type: 'is-danger' })
      Sentry.captureException(e)
    }
    return null
  }

  private async createCharacter(): Promise<Character | null> {
    if (this.character !== null) return this.character
    const char = await this.importCharacter()
    if (char === null) return null

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
        char.id = json.id
        return char
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
    return null
  }

  public async createCharAndBIS(tier: Tier): Promise<boolean> {
    if (this.checkFieldsHaveValidURLs()) return false

    const char = await this.createCharacter()
    // It'll be an error
    if (char === null) return false
    this.character = char
    this.characterLoaded = true

    // TODO - Make BIS stuff
    const bis = await this.createBIS(tier)
    if (bis === null) return false
    this.bisList = bis
    this.bisLoaded = true

    // State Refresh. When form is used, it should block changing the page.
    this.$store.dispatch('fetchCharacters')
    return true
  }

  private getCraftedCurrentGear(tier: Tier): LodestoneImportResponse {
    const craftedIl = tier.max_item_level - 25
    const gearType = this.$store.state.gear.find((g: Gear) => g.item_level === craftedIl && g.has_weapon && g.has_armour && g.has_accessories)!
    return {
      job_id: '',
      mainhand: gearType.id,
      offhand: gearType.id,
      head: gearType.id,
      body: gearType.id,
      hands: gearType.id,
      legs: gearType.id,
      feet: gearType.id,
      earrings: gearType.id,
      necklace: gearType.id,
      bracelet: gearType.id,
      left_ring: gearType.id,
      right_ring: gearType.id,
      min_il: craftedIl,
      max_il: craftedIl,
    }
  }

  private async importBISGear(): Promise<ExternalBISGearImportResponse | null> {
    // Pass the request to either the Etro or XIVGear method where appropriate
    const bisUrl = this.bisUrl()
    if (this.etroUrlRegex.exec(bisUrl) !== null) return this.importEtroBISGear()
    if (this.xivGearUrlRegex.exec(bisUrl) !== null) return this.importXIVGearBISGear()
    return null
  }

  private async importEtroBISGear(): Promise<ExternalBISGearImportResponse | null> {
    const etroUrl = this.bisUrl()
    const match = this.etroUrlRegex.exec(etroUrl)
    if (match === null) return null
    const url = `/backend/api/import/etro/${match[1]}/`
    try {
      const response = await fetch(url)
      if (response.ok) {
        // Handle the import
        const data = await response.json() as ExternalBISGearImportResponse
        return data
      }
      const error = await response.json() as ImportError
      this.bisUrlErrors = [error.message]
    }
    catch (e) {
      this.$notify({ text: `Error ${e} when attempting to import Etro data.`, type: 'is-danger' })
      Sentry.captureException(e)
    }
    return null
  }

  async importXIVGearBISGear(): Promise<ExternalBISGearImportResponse | null> {
    const xivGearUrl = this.bisUrl()
    const match = this.xivGearUrlRegex.exec(xivGearUrl)
    if (match === null) return null
    const url = `/backend/api/import/xivgear/${match[1]}/`

    try {
      const response = await fetch(url)
      if (response.status === 200) {
        // Handle the import
        const data = await response.json() as ExternalBISGearImportResponse
        return data
      }
      if (response.status === 202) {
        // Warn the user that the Sheet Selection is not supported on this page, and ask them to re-export the single set
        this.bisUrlErrors = [
          'The provided XIVGear URL contains multiple sets.',
          'This page does not provide the ability to select a set from your sheet.',
          'Please either Export a single set url from XIVGear, or import the BIS manually on your Character\'s page!.',
        ]
      }
      else if (!response.ok) {
        const error = await response.json() as ImportError
        this.bisUrlErrors = [error.message]
      }
    }
    catch (e) {
      this.$notify({ text: `Error ${e} when attempting to import XIVGear data.`, type: 'is-danger' })
      Sentry.captureException(e)
    }
    return null
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

  private async importCurrentGear(jobId: string, tier: Tier): Promise<LodestoneImportResponse | null> {
    try {
      const response = await fetch(`/backend/api/lodestone/${this.character!.lodestone_id}/import/${jobId}`)
      if (response.ok) {
        // Handle the import
        const data = await response.json() as LodestoneImportResponse
        return data
      }
      if (response.status === 406) {
        // Couldn't import because of wrong job, generate tier crafted
        return this.getCraftedCurrentGear(tier)
      }
      // Only add the "Error while ..." text when it's not for the wrong job error
      const error = await response.json() as ImportError
      this.$notify({ text: `Error while importing Lodestone gear; ${error.message}`, type: 'is-danger' })
    }
    catch (e) {
      this.$notify({ text: `Error ${e} when attempting to import Lodestone data.`, type: 'is-danger' })
      Sentry.captureException(e)
    }
    return null
  }
}
</script>

<style lang="scss">
</style>
