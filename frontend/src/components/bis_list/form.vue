<template>
  <div>
    <BISListDesktopForm
      :bisList="bisList"
      :character="character"
      :errors="errors"
      :displayOffhand="displayOffhand"
      :minIl="minIl"
      :maxIl="maxIl"
      :method="method"
      :url="url"
      v-on:update-min-il="updateMinIl"
      v-on:update-max-il="updateMaxIl"
      v-on:error-code="emitErrorCode"
      v-on:errors="handleErrors"
      v-on:save="$emit('save')"
      v-on:close="$emit('close')"
      v-on:import-bis-data="importBISData"

      v-if="renderDesktop"
    />

    <BISListMobileForm
      :bisList="bisList"
      :character="character"
      :errors="errors"
      :displayOffhand="displayOffhand"
      :minIl="minIl"
      :maxIl="maxIl"
      :method="method"
      :url="url"
      :simpleActions="!renderDesktop"
      v-on:update-min-il="updateMinIl"
      v-on:update-max-il="updateMaxIl"
      v-on:error-code="emitErrorCode"
      v-on:errors="handleErrors"
      v-on:save="$emit('save')"
      v-on:close="$emit('close')"
      v-on:import-bis-data="importBISData"
      :class="[renderDesktop ? 'is-hidden-desktop' : '']"
    />
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'
import BISListDesktopForm from '@/components/bis_list/desktop_form.vue'
import BISListMobileForm from '@/components/bis_list/mobile_form.vue'
import BISListModify from '@/dataclasses/bis_list_modify'
import { CharacterDetails } from '@/interfaces/character'
import { ImportResponse } from '@/interfaces/imports'
import { BISListErrors } from '@/interfaces/responses'

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

  errors: BISListErrors = {}

  @Prop()
  method!: string

  @Prop({ default: true })
  renderDesktop!: boolean

  @Prop()
  url!: string

  // Set up default values for min and max IL, will change as new tiers are released
  maxIl = 605

  minIl = 580

  updateMinIl(minIl: number): void {
    this.minIl = minIl
  }

  updateMaxIl(maxIl: number): void {
    this.maxIl = maxIl
  }

  emitErrorCode(errorCode: number): void {
    this.$emit('error-code', errorCode)
  }

  handleErrors(errors: BISListErrors): void {
    this.errors = errors
  }

  importBISData(data: ImportResponse): void {
    if (data.min_il < this.minIl) this.minIl = data.min_il
    if (data.max_il > this.maxIl) this.maxIl = data.max_il
    Vue.nextTick(() => {
      this.bisList.importBIS(data)
      this.displayOffhand = data.job_id === 'PLD'
      this.$forceUpdate()
    })
  }

  mounted(): void {
    this.displayOffhand = this.bisList.job_id === 'PLD'
  }
}
</script>

<style lang="scss">
</style>
