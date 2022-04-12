<template>
  <div>
    <div v-if="!loaded">
      <button class="button is-static is-loading is-fullwidth">Loading</button>
    </div>
    <div v-else>
      <div class="breadcrumb">
        <ul>
          <li><router-link :to="`/characters/${character.id}/`">{{ character.name }} @ {{ character.world }}</router-link></li>
          <li class="is-active"><a aria-current="page">{{ breadcrumb }}</a></li>
        </ul>
      </div>
      <BISListForm :bisList="bisList" :errors="errors" />
      <button class="button is-fullwidth is-success" @click="save">Save</button>
    </div>
  </div>
</template>

<script lang="ts">
import { Component } from 'vue-property-decorator'
import BISListForm from '@/components/bis_list_form.vue'
import BISListModify from '@/dataclasses/bis_list_modify'
import BISList from '@/interfaces/bis_list'
import { BISListErrors } from '@/interfaces/responses'
import NewBIS from './new_bis.vue'

@Component({
  components: {
    BISListForm,
  },
})
export default class EditBIS extends NewBIS {
  // Flags and URLS
  listLoaded = false

  // Data
  bisList!: BISListModify

  breadcrumb!: string

  // Flag indicating if we're ready to display the page
  get loaded(): boolean {
    if (this.charLoaded && this.listLoaded) {
      document.title = `Edit ${this.bisList.job_id} - ${this.character.name} - Savage Aim`
      return true
    }
    return false
  }

  // URL for reading and writing
  get url(): string {
    return `/backend/api/character/${this.$route.params.characterId}/bis_lists/${this.$route.params.id}/`
  }

  // Load functions
  async getList(): Promise<void> {
    try {
      const response = await fetch(this.url)
      if (response.ok) {
        // Parse the list into an array of character interfaces and store them in the character data list
        const data = await response.json() as BISList
        this.bisList = BISListModify.buildEditVersion(data)
        this.breadcrumb = this.bisList.job_id
        this.listLoaded = true
      }
      else {
        super.handleError(response.status)
      }
    }
    catch (e) {
      this.$notify({ text: `Error ${e} when fetching BIS List.`, type: 'is-danger' })
    }
  }

  // Populate the data
  created(): void {
    this.load()
  }

  async load(): Promise<void> {
    this.getChar()
    this.getList()
  }

  // Save the data into a new bis list
  async save(): Promise<void> {
    const body = JSON.stringify(this.bisList)
    try {
      const response = await fetch(this.url, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': this.$cookies.get('csrftoken'),
        },
        body,
      })

      if (response.ok) {
        this.$notify({ text: 'Successfully updated!', type: 'is-success' })
      }
      else {
        super.handleError(response.status)
        this.errors = (await response.json() as BISListErrors)
      }
    }
    catch (e) {
      this.$notify({ text: `Error ${e} when attempting to update BIS List.`, type: 'is-danger' })
    }
  }
}
</script>

<style lang="scss">
</style>
