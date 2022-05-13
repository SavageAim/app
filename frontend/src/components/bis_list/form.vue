<template>
  <div>
    <BISListDesktopForm
      :bisList="bisList"
      :errors="errors"
      :displayOffhand="displayOffhand"
      :minIl="minIl"
      :maxIl="maxIl"
      :method="method"
      :url="url"
      v-on:job-change="jobChange"
      v-on:update-min-il="updateMinIl"
      v-on:update-max-il="updateMaxIl"
      v-on:error-code="emitErrorCode"
      v-on:errors="handleErrors"
      v-on:save="emitSave"

      v-if="renderDesktop"
    />

    <BISListMobileForm
      :bisList="bisList"
      :errors="errors"
      :displayOffhand="displayOffhand"
      :minIl="minIl"
      :maxIl="maxIl"
      :method="method"
      :url="url"
      v-on:job-change="jobChange"
      v-on:update-min-il="updateMinIl"
      v-on:update-max-il="updateMaxIl"
      v-on:error-code="emitErrorCode"
      v-on:errors="handleErrors"
      v-on:save="emitSave"
      :class="[renderDesktop ? 'is-hidden-desktop' : '']"
    />
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'
import BISListDesktopForm from '@/components/bis_list/desktop_form.vue'
import BISListMobileForm from '@/components/bis_list/mobile_form.vue'
import BISListModify from '@/dataclasses/bis_list_modify'
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

  // Handle the events that change values
  jobChange(selectedJob: string): void {
    this.displayOffhand = selectedJob === 'paladin'
    this.$forceUpdate()
  }

  updateMinIl(minIl: number): void {
    this.minIl = minIl
  }

  updateMaxIl(maxIl: number): void {
    this.maxIl = maxIl
  }

  emitErrorCode(errorCode: number): void {
    this.$emit('error-code', errorCode)
  }

  emitSave(): void {
    this.$emit('save')
  }

  handleErrors(errors: BISListErrors): void {
    this.errors = errors
  }
}
</script>

<style lang="scss">
.mobile-form {
  margin-bottom: 1rem;
}
</style>
