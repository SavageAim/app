<template>
  <div class="field is-horizontal">
    <div class="field-label is-normal">
      <label class="label">{{ name }}</label>
    </div>
    <div class="field-body">
      <div class="field">
        <div class="control">
          <div class="select is-fullwidth" :class="{'is-danger': error !== undefined}">
            <select ref="dropdown" :value="value" @input="handleInput">
              <option value="-1">Select Gear</option>
              <option v-for="gear in choices" :key="gear.id" :value="gear.id">{{ gear.name }} ({{ gear.item_level }})</option>
            </select>
          </div>
        </div>
        <p v-if="error !== undefined" class="help is-danger">{{ error[0] }}</p>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'
import Gear from '@/interfaces/gear'

@Component
export default class GearDropdown extends Vue {
  @Prop()
  choices!: Gear[]

  @Prop()
  error!: string[] | undefined

  @Prop()
  name!: string

  @Prop()
  value!: number

  get dropdown(): HTMLSelectElement {
    return this.$refs.dropdown as HTMLSelectElement
  }

  handleInput(): void {
    this.$emit('input', this.dropdown.value)
  }
}
</script>

<style lang="scss">
</style>
