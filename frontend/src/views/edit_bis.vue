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
          <li class="is-active"><a aria-current="page">{{ breadcrumb }}</a></li>
        </ul>
      </div>
      <BISListForm :bisList="bisList" :character="character" :url="url" method="PUT" v-on:error-code="handleError" v-on:save="postSave" />
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop } from 'vue-property-decorator'
import BISListForm from '@/components/bis_list/form.vue'
import BISListModify from '@/dataclasses/bis_list_modify'
import BISList from '@/interfaces/bis_list'
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
  @Prop()
  bisId!: number

  bisList!: BISListModify

  breadcrumb!: string

  @Prop()
  characterId!: number

  // Flag indicating if we're ready to display the page
  get loaded(): boolean {
    if (this.charLoaded && this.listLoaded) {
      document.title = `Edit ${this.bisList.display_name} - ${this.character.name} - Savage Aim`
      return true
    }
    return false
  }

  // URL for reading and writing
  get url(): string {
    return `/backend/api/character/${this.characterId}/bis_lists/${this.bisId}/`
  }

  // Load functions
  async getList(): Promise<void> {
    try {
      const response = await fetch(this.url)
      if (response.ok) {
        // Parse the list into an array of character interfaces and store them in the character data list
        const data = await response.json() as BISList
        this.bisList = BISListModify.buildEditVersion(data)
        this.updateBreadcrumb()
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

  updateBreadcrumb(): void {
    this.breadcrumb = this.bisList.display_name
  }

  async postSave(): Promise<void> {
    await this.getList()
    this.updateBreadcrumb()
  }
}
</script>

<style lang="scss">
</style>
