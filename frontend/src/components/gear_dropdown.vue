<template>
  <div class="field is-horizontal">
    <div class="field-label is-normal">
      <label class="label">{{ name }}</label>
    </div>
    <template v-if="bisValue">
      <div class="field-body">
        <div class="field is-expanded">
          <div class="field has-addons">
            <div class="control is-expanded">
              <div class="select is-fullwidth" :class="{'is-danger': error !== undefined}">
                <select ref="dropdown" :value="value" @input="handleInput">
                  <option value="-1">Select Gear</option>
                  <option v-for="item in gear" :key="item.id" :value="item.id">{{ item.name }} ({{ item.item_level }})</option>
                </select>
              </div>
            </div>
            <div class="control">
              <button class="button is-link" @click="setToCopyValue" data-microtip-position="top" role="tooltip" aria-label="Paste BIS Value">
                <i class="material-icons">content_paste_go</i>
              </button>
            </div>
            <p v-if="error !== undefined" class="help is-danger">{{ error[0] }}</p>
          </div>
        </div>
      </div>
    </template>
    <template v-else>
      <div class="field-body">
        <div class="field">
          <div class="control">
            <div class="select is-fullwidth" :class="{'is-danger': error !== undefined}">
              <select ref="dropdown" :value="value" @input="handleInput">
                <option value="-1">Select Gear</option>
                <option v-for="item in gear" :key="item.id" :value="item.id">{{ item.name }} ({{ item.item_level }})</option>
              </select>
            </div>
          </div>
          <p v-if="error !== undefined" class="help is-danger">{{ error[0] }}</p>
        </div>
      </div>
    </template>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'
import Gear from '@/interfaces/gear'

@Component
export default class GearDropdown extends Vue {
  @Prop()
  bisValue!: number | undefined

  @Prop()
  choices!: Gear[]

  @Prop()
  error!: string[] | undefined

  @Prop()
  maxIl!: number

  @Prop()
  minIl!: number

  @Prop()
  name!: string

  @Prop()
  value!: number

  get dropdown(): HTMLSelectElement {
    return this.$refs.dropdown as HTMLSelectElement
  }

  get gear(): Gear[] {
    return this.choices.filter((item: Gear) => item.id === this.value || item.id === this.bisValue || (item.item_level <= this.maxIl && item.item_level >= this.minIl))
  }

  handleInput(): void {
    this.$emit('input', this.dropdown.value)
  }

  setToCopyValue(): void {
    if (this.bisValue == null) return
    this.dropdown.value = `${this.bisValue}`
    this.handleInput()
  }
}
</script>

<style lang="scss">
</style>
