<template>
  <div>
    <BISListDesktopForm
      :bisList="bisList"
      :character="character"
      :char-is-proxy="charIsProxy"
      :errors="errors"
      :etro-importable="etroImportUrl() !== null"
      :import-loading="importLoading"
      :displayOffhand="displayOffhand"
      :minIl="minIl"
      :maxIl="maxIl"
      :method="method"
      :syncable="syncable()"
      :url="url"
      v-on:job-change="jobChange"
      v-on:update-ilevels="updateItemLevels"
      v-on:error-code="emitErrorCode"
      v-on:errors="handleErrors"
      v-on:save="$emit('save')"
      v-on:close="$emit('close')"
      v-on:import-bis-data="etroImport"
      v-on:import-current-data="displayLoadModal"
      v-on:import-current-lodestone-gear="lodestoneImport"

      v-if="renderDesktop"
    />

    <BISListMobileForm
      :bisList="bisList"
      :character="character"
      :char-is-proxy="charIsProxy"
      :errors="errors"
      :etro-importable="etroImportUrl() !== null"
      :import-loading="importLoading"
      :displayOffhand="displayOffhand"
      :minIl="minIl"
      :maxIl="maxIl"
      :method="method"
      :syncable="syncable()"
      :url="url"
      :simpleActions="!renderDesktop"
      v-on:job-change="jobChange"
      v-on:update-ilevels="updateItemLevels"
      v-on:error-code="emitErrorCode"
      v-on:errors="handleErrors"
      v-on:save="$emit('save')"
      v-on:close="$emit('close')"
      v-on:import-bis-data="etroImport"
      v-on:import-current-data="displayLoadModal"
      v-on:import-current-lodestone-gear="lodestoneImport"
      :class="[renderDesktop ? 'is-hidden-desktop' : '']"
    />
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
import BISListDesktopForm from '@/components/bis_list/desktop_form.vue'
import BISListMobileForm from '@/components/bis_list/mobile_form.vue'
import BISListModify from '@/dataclasses/bis_list_modify'
import BISList from '@/interfaces/bis_list'
import { CharacterDetails } from '@/interfaces/character'
import { EtroImportResponse, ImportError, LodestoneImportResponse } from '@/interfaces/imports'
import { BISListErrors } from '@/interfaces/responses'
import LoadCurrentGear from '../modals/load_current_gear.vue'

@Component({
  components: {
    BISListDesktopForm,
    BISListMobileForm,
  },
})
export default class BISListForm extends Vue {
  displayOffhand = true

  @Prop()
  bisList!: BISListModify

  @Prop()
  character!: CharacterDetails

  @Prop({ default: false })
  charIsProxy!: boolean

  etroImportPattern = /https:\/\/etro\.gg\/gearset\/([-a-z0-9]+)\/?/

  @Prop({ default() { return {} } })
  externalErrors!: BISListErrors

  importLoading = false

  internalErrors: BISListErrors = {}

  @Prop()
  method!: string

  @Prop({ default: true })
  renderDesktop!: boolean

  @Prop()
  url!: string

  // Set up default values for min and max IL, will change as new tiers are released
  maxIl = this.$store.state.maxItemLevel

  minIl = this.maxIl - 25

  get errors(): BISListErrors {
    return {
      ...this.internalErrors,
      ...this.externalErrors,
    }
  }

  get lodestoneImportUrl(): string {
    return `/backend/api/lodestone/${this.character.lodestone_id}/import`
  }

  get syncableLists(): BISList[] {
    if (this.character.bis_lists == null) return []
    return this.character.bis_lists.filter((list: BISList) => list.id !== this.bisList.id && list.job.id === this.bisList.job_id)
  }

  calculateCurrentILRange(data: BISList): { minIl: number, maxIl: number } {
    const itemLevels = [
      data.current_mainhand.item_level,
      data.current_offhand.item_level,
      data.current_head.item_level,
      data.current_body.item_level,
      data.current_hands.item_level,
      data.current_legs.item_level,
      data.current_feet.item_level,
      data.current_earrings.item_level,
      data.current_necklace.item_level,
      data.current_bracelet.item_level,
      data.current_left_ring.item_level,
      data.current_right_ring.item_level,
    ]

    return { minIl: Math.min(...itemLevels), maxIl: Math.max(...itemLevels) }
  }

  displayLoadModal(): void {
    this.$modal.show(LoadCurrentGear, { bisLists: this.syncableLists, loadBIS: this.importCurrentData })
  }

  emitErrorCode(errorCode: number): void {
    this.$emit('error-code', errorCode)
  }

  async etroImport(): Promise<void> {
    const url = this.etroImportUrl()
    if (url === null) return
    this.importLoading = true
    try {
      const response = await fetch(url)
      if (response.ok) {
        // Handle the import
        const data = await response.json() as EtroImportResponse
        this.importBISData(data)
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

  @Watch('bisList.external_link', { deep: true })
  etroImportUrl(): string | null {
    const match = this.etroImportPattern.exec(this.bisList.external_link || '')
    if (match === null) return null
    return `/backend/api/import/etro/${match[1]}/`
  }

  handleErrors(errors: BISListErrors): void {
    this.internalErrors = errors
  }

  importBISData(data: EtroImportResponse): void {
    if (data.min_il < this.minIl) this.minIl = data.min_il
    if (data.max_il > this.maxIl) this.maxIl = data.max_il
    Vue.nextTick(() => {
      this.bisList.importBIS(data)
      this.jobChange(data.job_id)
      this.$forceUpdate()
      this.$notify({ text: 'Successfully imported BIS Gear!', type: 'is-success' })
    })
  }

  importCurrentData(data: BISList): void {
    // Calculate min and max item levels
    const { minIl, maxIl } = this.calculateCurrentILRange(data)
    if (minIl < this.minIl) this.minIl = minIl
    if (maxIl > this.maxIl) this.maxIl = maxIl
    Vue.nextTick(() => {
      this.bisList.importCurrent(data)
      this.$forceUpdate()
      this.$notify({ text: 'Successfully imported Current Gear!', type: 'is-success' })
    })
  }

  importCurrentLodestoneGear(data: LodestoneImportResponse): void {
    if (data.min_il < this.minIl) this.minIl = data.min_il
    if (data.max_il > this.maxIl) this.maxIl = data.max_il
    Vue.nextTick(() => {
      this.bisList.importCurrentLodestoneGear(data)
      this.$forceUpdate()
      this.$notify({ text: 'Successfully imported Current Gear from Lodestone!', type: 'is-success' })
    })
  }

  jobChange(selectedJob: string): void {
    this.displayOffhand = selectedJob === 'PLD'
  }

  async lodestoneImport(): Promise<void> {
    this.importLoading = true
    try {
      const response = await fetch(`${this.lodestoneImportUrl}/${this.bisList.job_id}`)
      if (response.ok) {
        // Handle the import
        const data = await response.json() as LodestoneImportResponse
        this.importCurrentLodestoneGear(data)
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

  mounted(): void {
    this.displayOffhand = this.bisList.job_id === 'PLD'
  }

  @Watch('bisList.job_id', { deep: true })
  syncable(): boolean {
    return this.syncableLists.length > 0
  }

  updateItemLevels(values: number[]): void {
    // Always comes in as [min, max]
    [this.minIl, this.maxIl] = values
  }
}
</script>

<style lang="scss">
</style>
