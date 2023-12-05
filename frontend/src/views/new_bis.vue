<template>
  <div>
    <div v-if="!loaded">
      <button class="button is-static is-loading is-fullwidth">Loading</button>
    </div>
    <div v-else>
      <div class="breadcrumb">
        <ul>
          <li><router-link :to="`/characters/${character.id}/`">{{ character.name }} @ {{ character.world }}</router-link></li>
          <li class="is-active"><a href="#">BIS Lists</a></li>
          <li class="is-active"><a aria-current="page">New</a></li>
        </ul>
      </div>
      <BISListForm :bisList="bisList" :character="character" :url="url" method="POST" v-on:error-code="handleError" />
    </div>
  </div>
</template>

<script lang="ts">
import * as Sentry from '@sentry/vue'
import { Component, Prop } from 'vue-property-decorator'
import BISListForm from '@/components/bis_list/form.vue'
import BISListModify from '@/dataclasses/bis_list_modify'
import { CharacterDetails } from '@/interfaces/character'
import SavageAimMixin from '@/mixins/savage_aim_mixin'

@Component({
  components: {
    BISListForm,
  },
})
export default class NewBIS extends SavageAimMixin {
  // Flags and URLS
  charLoaded = false

  // Data
  bisList = new BISListModify()

  character!: CharacterDetails

  @Prop()
  characterId!: number

  // URL to load character data from
  get charUrl(): string {
    return `/backend/api/character/${this.characterId}/`
  }

  // Flag indicating if we're ready to display the page
  get loaded(): boolean {
    if (this.charLoaded) {
      document.title = `New BIS - ${this.character.name} - Savage Aim`
    }
    return this.charLoaded
  }

  // Url to send data to
  get url(): string {
    return `/backend/api/character/${this.characterId}/bis_lists/`
  }

  // Load functions
  async getChar(): Promise<void> {
    try {
      const response = await fetch(this.charUrl)
      if (response.ok) {
        // Parse the list into an array of character interfaces and store them in the character data list
        this.character = (await response.json()) as CharacterDetails
        this.charLoaded = true
      }
      else {
        super.handleError(response.status)
      }
    }
    catch (e) {
      this.$notify({ text: `Error ${e} when fetching Character.`, type: 'is-danger' })
      Sentry.captureException(e)
    }
  }

  // Populate the data
  created(): void {
    this.getChar()
  }

  handleError(errorCode: number): void {
    super.handleError(errorCode)
  }
}
</script>

<style lang="scss">
</style>
