<template>
  <div class="card-content">
    <div class="buttons">
      <button v-if="!charIsProxy" class="button is-fullwidth is-success" data-microtip-position="top" role="tooltip" :aria-label="`${saveText} this BIS List.`" @click="save">
        <span class="icon-text">
          <span class="icon"><i class="material-icons">save</i></span>
          <span>{{ saveText }} BIS List</span>
        </span>
      </button>

      <template v-if="!(simple || charIsProxy)">
        <button class="button is-fullwidth is-success" data-microtip-position="top" role="tooltip" :aria-label="`${saveText} this BIS List, and sync current gear to other ${bisList.job_id} BIS Lists.`" v-if="syncable()" @click="displaySyncModal">
          <span class="icon-text">
            <span class="icon"><i class="material-icons">save_as</i></span>
            <span>{{ saveText }} &amp; Sync Current Gear</span>
          </span>
        </button>
        <button class="button is-fullwidth is-disabled" data-microtip-position="top" role="tooltip" :aria-label="`You have no other ${bisList.job_id} BIS Lists.`" v-else>
          <span class="icon-text">
            <span class="icon"><i class="material-icons">save_as</i></span>
            <span>{{ saveText }} &amp; Sync Current Gear</span>
          </span>
        </button>
      </template>

      <template v-if="!importLoading">
        <button class="button is-fullwidth is-primary" data-microtip-position="top" role="tooltip" aria-label="Import BIS Gear from Etro.gg" v-if="importable()" @click="etroImport">
          <span class="icon-text">
            <span class="icon"><i class="material-icons">download</i></span>
            <span>Import from Etro</span>
          </span>
        </button>
        <button class="button is-fullwidth is-disabled" data-microtip-position="top" role="tooltip" aria-label="Please enter an Etro gearset link in the external URL." v-else>
          <span class="icon-text">
            <span class="icon"><i class="material-icons">download</i></span>
            <span>Import from Etro</span>
          </span>
        </button>
      </template>
      <button v-else class="button is-static is-loading is-fullwidth">Loading data.</button>

      <template v-if="!(simple || charIsProxy)">
        <button class="button is-fullwidth is-primary" data-microtip-position="top" role="tooltip" :aria-label="`Load Current gear from another ${bisList.job_id} BIS List.`" v-if="syncable()" @click="displayLoadModal">
          <span class="icon-text">
            <span class="icon"><i class="material-icons">content_copy</i></span>
            <span>Copy Current Gear</span>
          </span>
        </button>
        <button class="button is-fullwidth is-disabled" data-microtip-position="top" role="tooltip" :aria-label="`You have no other ${bisList.job_id} BIS Lists.`" v-else>
          <span class="icon-text">
            <span class="icon"><i class="material-icons">content_copy</i></span>
            <span>Copy Current Gear</span>
          </span>
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
import { ImportResponse, ImportError } from '@/interfaces/imports'

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

  importPattern = /https:\/\/etro\.gg\/gearset\/([-a-z0-9]+)\/?/

  get create(): boolean {
    return this.method === 'POST'
  }

  get etroImportUrl(): string | null {
    const match = this.importPattern.exec(this.bisList.external_link || '')
    if (match === null) return null
    return `/backend/api/import/etro/${match[1]}/`
  }

  get saveText(): string {
    if (this.create) return 'Create'
    return 'Save'
  }

  get syncableLists(): BISList[] {
    if (this.character.bis_lists == null) return []
    return this.character.bis_lists.filter((list: BISList) => list.id !== this.bisList.id && list.job.id === this.bisList.job_id)
  }

  @Watch('bisList.external_link', { deep: true })
  importable(): boolean {
    return this.importPattern.exec(this.bisList.external_link || '') !== null
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

  async etroImport(): Promise<void> {
    const url = this.etroImportUrl
    if (url === null) return
    this.importLoading = true
    try {
      const response = await fetch(url)
      if (response.ok) {
        // Handle the import
        const data = await response.json() as ImportResponse
        this.$emit('import-bis-data', data)
      }
      else {
        const error = await response.json() as ImportError
        this.$notify({ text: `Error while importing Etro gearset; ${error.message}`, type: 'is-danger' })
      }
    }
    catch (e) {
      this.$notify({ text: `Error ${e} when attempting to import Etro data.`, type: 'is-danger' })
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
