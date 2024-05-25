<template>
  <div class="card-content">
    <div class="buttons">
      <button v-if="!charIsProxy" class="button is-fullwidth is-success" data-microtip-position="top" role="tooltip" :aria-label="`${saveText} this BIS List.`" @click="save">
        <span class="icon"><i class="material-icons">save</i></span>
        <span>{{ saveText }} BIS List</span>
      </button>

      <template v-if="!(simple || charIsProxy)">
        <button class="button is-fullwidth is-success" data-microtip-position="top" role="tooltip" :aria-label="`${saveText} this BIS List, and sync current gear to other ${bisList.job_id} BIS Lists.`" v-if="syncable()" @click="displaySyncModal">
          <span class="icon"><i class="material-icons">save_as</i></span>
          <span>{{ saveText }} &amp; Sync Current Gear</span>
        </button>
        <button class="button is-fullwidth is-disabled" data-microtip-position="top" role="tooltip" :aria-label="`You have no other ${bisList.job_id} BIS Lists.`" v-else>
          <span class="icon"><i class="material-icons">save_as</i></span>
          <span>{{ saveText }} &amp; Sync Current Gear</span>
        </button>
      </template>

      <button class="button is-fullwidth is-link" data-microtip-position="top" role="tooltip" aria-label="Import Current Gear from Lodestone" @click="lodestoneImport" v-if="!importLoading">
        <span class="icon"><i class="material-icons">cloud_download</i></span>
        <span>Import from Lodestone</span>
      </button>
      <button v-else class="button is-static is-loading is-fullwidth">Loading data.</button>

      <template v-if="!(simple || charIsProxy)">
        <button class="button is-fullwidth is-link" data-microtip-position="top" role="tooltip" :aria-label="`Load Current gear from another ${bisList.job_id} BIS List.`" v-if="syncable()" @click="displayLoadModal">
          <span class="icon"><i class="material-icons">content_copy</i></span>
          <span>Copy Current Gear</span>
        </button>
        <button class="button is-fullwidth is-disabled" data-microtip-position="top" role="tooltip" :aria-label="`You have no other ${bisList.job_id} BIS Lists.`" v-else>
          <span class="icon"><i class="material-icons">content_copy</i></span>
          <span>Copy Current Gear</span>
        </button>
      </template>
    </div>
  </div>
</template>

<script lang="ts">
import * as Sentry from '@sentry/vue'
import {
  Component,
  Prop,
  Vue,
  Watch,
} from 'vue-property-decorator'
import LoadCurrentGear from '@/components/modals/load_current_gear.vue'
import SyncCurrentGear from '@/components/modals/sync_current_gear.vue'
import BISListModify from '@/dataclasses/bis_list_modify'
import BISList from '@/interfaces/bis_list'
import { CharacterDetails } from '@/interfaces/character'
import { CreateResponse, BISListErrors } from '@/interfaces/responses'
import { ImportError, LodestoneImportResponse } from '@/interfaces/imports'

@Component
export default class Actions extends Vue {
  @Prop()
  bisList!: BISListModify

  @Prop()
  character!: CharacterDetails

  @Prop()
  charIsProxy!: boolean

  importLoading = false

  @Prop()
  method!: string

  // Hide actions that spawn popups when this flag is true
  @Prop({ default: false })
  simple!: boolean

  @Prop()
  url!: string

  get create(): boolean {
    return this.method === 'POST'
  }

  get lodestoneImportUrl(): string {
    return `/backend/api/lodestone/${this.character.lodestone_id}/import`
  }

  get saveText(): string {
    if (this.create) return 'Create'
    return 'Save'
  }

  get syncableLists(): BISList[] {
    if (this.character.bis_lists == null) return []
    return this.character.bis_lists.filter((list: BISList) => list.id !== this.bisList.id && list.job.id === this.bisList.job_id)
  }

  @Watch('bisList.job_id', { deep: true })
  syncable(): boolean {
    return this.syncableLists.length > 0
  }

  displayLoadModal(): void {
    this.$modal.show(LoadCurrentGear, { bisLists: this.syncableLists, loadBIS: this.loadCurrentGearFromList })
  }

  displaySyncModal(): void {
    this.$modal.show(SyncCurrentGear, { bisLists: this.syncableLists, save: this.saveAndSync, verb: this.saveText })
  }

  loadCurrentGearFromList(list: BISList): void {
    this.$emit('import-current-data', list)
  }

  async lodestoneImport(): Promise<void> {
    this.importLoading = true
    try {
      const response = await fetch(`${this.lodestoneImportUrl}/${this.bisList.job_id}`)
      if (response.ok) {
        // Handle the import
        const data = await response.json() as LodestoneImportResponse
        this.$emit('import-current-lodestone-gear', data)
      }
      else {
        const error = await response.json() as ImportError
        if (response.status === 406) {
          this.$notify({ text: error.message, type: 'is-link' })
        }
        else {
          // Only add the "Error while ..." text when it's not for the wrong job error
          this.$notify({ text: `Error while importing Lodestone gear; ${error.message}`, type: 'is-danger' })
        }
      }
    }
    catch (e) {
      this.$notify({ text: `Error ${e} when attempting to import Lodestone data.`, type: 'is-danger' })
      Sentry.captureException(e)
    }
    finally {
      this.importLoading = false
    }
  }

  save(): void {
    // Send without syncing anything
    this.sendData(this.url)
  }

  saveAndSync(listIds: string[]): void {
    // Build up the search params
    const params = new URLSearchParams()
    listIds.forEach((id: string) => params.append('sync', id))
    this.sendData(`${this.url}?${params.toString()}`)
  }

  // Save the data into a new bis list
  async sendData(url: string): Promise<void> {
    this.$emit('errors', {})
    const body = JSON.stringify(this.bisList)
    try {
      const response = await fetch(url, {
        method: this.method,
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': this.$cookies.get('csrftoken'),
        },
        body,
      })

      if (response.ok) {
        if (this.simple) {
          this.$notify({ text: 'BIS List Created successfully!', type: 'is-success' })
          this.$emit('close')
        }
        else if (this.create) {
          // Redirect back to the new bis list page
          const json = await response.json() as CreateResponse
          this.$router.push(`./${json.id}/`, () => {
            Vue.notify({ text: 'BIS List Created successfully!', type: 'is-success' })
          })
        }
        else {
          this.$notify({ text: 'Successfully updated!', type: 'is-success' })
        }
        this.$emit('save')
      }
      else {
        // Emit events here to handle the error
        this.$emit('error-code', response.status)
        this.$emit('errors', await response.json() as BISListErrors)
      }
    }
    catch (e) {
      this.$notify({ text: `Error ${e} when attempting to create BIS List.`, type: 'is-danger' })
      Sentry.captureException(e)
    }
  }
}
</script>

<style lang="scss">
</style>
