<template>
  <div>
    <div v-if="!loaded">
      <button class="button is-static is-loading is-fullwidth">Loading</button>
    </div>
    <div v-else>
      <div class="breadcrumb">
        <ul>
          <li><router-link :to="`/characters/${character.id}/`">{{ character.name }} @ {{ character.world }}</router-link></li>
          <li class="is-active"><a aria-current="page">New BIS List</a></li>
        </ul>
      </div>
      <BISListForm :bisList="bisList" :jobs="jobs" :errors="errors" />
      <button class="button is-fullwidth is-success" @click="save">Create</button>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import BISListForm from '@/components/bis_list_form.vue'
import BISListModify from '@/dataclasses/bis_list_modify'
import { CreateResponse, BISListErrors } from '@/interfaces/responses'
import { CharacterDetails } from '@/interfaces/character'
import Job from '@/interfaces/job'
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

  errors: BISListErrors = {}

  // URL to load character data from
  get charUrl(): string {
    return `/backend/api/character/${this.$route.params.characterId}/`
  }

  // Get store elements
  get jobs(): Job[] {
    return this.$store.state.jobs
  }

  // Conversion getters for refs
  get jobPicker(): HTMLSelectElement {
    return this.$refs.jobPicker as HTMLSelectElement
  }

  get jobIcon(): HTMLImageElement {
    return this.$refs.jobIcon as HTMLImageElement
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
    return `/backend/api/character/${this.$route.params.characterId}/bis_lists/`
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
    }
  }

  // Populate the data
  created(): void {
    this.getChar()
  }

  // Save the data into a new bis list
  async save(): Promise<void> {
    const body = JSON.stringify(this.bisList)
    try {
      const response = await fetch(this.url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': this.$cookies.get('csrftoken'),
        },
        body,
      })

      if (response.ok) {
        // Redirect back to the new bis list page
        const json = await response.json() as CreateResponse
        this.$router.push(`./${json.id}/`, () => {
          Vue.notify({ text: `New BIS List created successfully!`, type: 'is-success' })
        })
      }
      else {
        super.handleError(response.status)
        this.errors = (await response.json() as BISListErrors)
      }
    }
    catch (e) {
      this.$notify({ text: `Error ${e} when attempting to create BIS List.`, type: 'is-danger' })
    }
  }
}
</script>

<style lang="scss">
</style>
