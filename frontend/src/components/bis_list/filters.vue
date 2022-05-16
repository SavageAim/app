<template>
  <div class="card-content">
    <div class="field is-horizontal">
      <div class="field-label is-normal">
        <label class="label">Min ILvl</label>
      </div>
      <div class="field-body">
        <div class="field">
          <div class="control">
            <div class="select is-fullwidth">
              <select ref="minIlPicker" @change="updateMin" :value="minIl">
                <option v-for="val in ilChoices" :key="val" :value="val">{{ val }}</option>
              </select>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="field is-horizontal">
      <div class="field-label is-normal">
        <label class="label">Max ILvl</label>
      </div>
      <div class="field-body">
        <div class="field">
          <div class="control">
            <div class="select is-fullwidth">
              <select ref="maxIlPicker" @change="updateMax" :value="maxIl">
                <option v-for="val in ilChoices" :key="val" :value="val">{{ val }}</option>
              </select>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'
import range from 'range-inclusive'

@Component
export default class Filters extends Vue {
  @Prop()
  maxIl!: number

  @Prop()
  minIl!: number

  // Get an array of item level choices based on the total min and max values
  get ilChoices(): number[] {
    return range(this.$store.state.maxItemLevel, this.$store.state.minItemLevel, -5)
  }

  // Ref converters
  get minIlPicker(): HTMLSelectElement {
    return this.$refs.minIlPicker as HTMLSelectElement
  }

  get maxIlPicker(): HTMLSelectElement {
    return this.$refs.maxIlPicker as HTMLSelectElement
  }

  updateMin(): void {
    this.$emit('update-min', this.minIlPicker.value)
  }

  updateMax(): void {
    this.$emit('update-max', this.maxIlPicker.value)
  }
}
</script>

<style lang="scss">
</style>
