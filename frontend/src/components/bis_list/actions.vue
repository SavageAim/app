<template>
  <div class="card-content">
    <div class="buttons">
      <button class="button is-fullwidth is-success" data-microtip-position="top" role="tooltip" :aria-label="`${saveText} this BIS List.`" @click="save">{{ saveText }} BIS List</button>

      <button class="button is-fullwidth is-success" data-microtip-position="top" role="tooltip" :aria-label="`${saveText} this BIS List, and sync current gear to other ${bisList.job_id} BIS Lists.`" v-if="syncable()">{{ saveText }} and Sync Current Gear</button>
      <button class="button is-fullwidth is-disabled" data-microtip-position="top" role="tooltip" aria-label="Please select a Job." v-else>{{ saveText }} and Sync Current Gear</button>

      <button class="button is-fullwidth is-primary" data-microtip-position="top" role="tooltip" aria-label="Import BIS Gear from Etro.gg" v-if="importable()">Import from Etro</button>
      <button class="button is-fullwidth is-disabled" data-microtip-position="top" role="tooltip" aria-label="Please enter an Etro gearset link in the external URL." v-else>Import</button>

      <button class="button is-fullwidth is-primary" data-microtip-position="top" role="tooltip" :aria-label="`Load Current gear from another ${bisList.job_id} BIS List.`" v-if="syncable()">Load Current Gear</button>
      <button class="button is-fullwidth is-disabled" data-microtip-position="top" role="tooltip" aria-label="Please select a Job." v-else>Load Current Gear</button>
    </div>
  </div>
</template>

<script lang="ts">
import {
  Component,
  Prop,
  Vue,
  Watch,
} from 'vue-property-decorator'
import BISListModify from '@/dataclasses/bis_list_modify'
import { CreateResponse, BISListErrors } from '@/interfaces/responses'

@Component
export default class Actions extends Vue {
  @Prop()
  bisList!: BISListModify

  @Prop()
  method!: string

  @Prop()
  url!: string

  importPattern = /https:\/\/etro\.gg\/gearset\/([-a-z0-9]+)\/?/

  get create(): boolean {
    return this.method === 'POST'
  }

  get saveText(): string {
    if (this.create) return 'Create'
    return 'Save'
  }

  @Watch('bisList.external_link', { deep: true })
  importable(): boolean {
    return this.importPattern.exec(this.bisList.external_link || '') !== null
  }

  @Watch('bisList.job_id', { deep: true })
  syncable(): boolean {
    return this.bisList.job_id !== 'na'
  }

  // Save the data into a new bis list
  async save(): Promise<void> {
    this.$emit('errors', {})
    const body = JSON.stringify(this.bisList)
    try {
      const response = await fetch(this.url, {
        method: this.method,
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': this.$cookies.get('csrftoken'),
        },
        body,
      })

      if (response.ok) {
        if (this.create) {
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
    }
  }
}
</script>

<style lang="scss">
</style>
