<template>
  <div class="card-content filter-card">
    <div class="field">
      <label class="label">Item Level</label>
      <div class="field-body">
        <div class="field">
          <div class="control">
            <div ref="iLevelSlider"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import noUiSlider, { PipsMode } from 'nouislider'
import { Component, Prop, Vue } from 'vue-property-decorator'

@Component
export default class Filters extends Vue {
  @Prop()
  maxIl!: number

  @Prop()
  minIl!: number

  mounted(): void {
    const container = this.$refs.iLevelSlider as HTMLElement
    const step = 5

    const slider = noUiSlider.create(container, {
      range: {
        min: this.$store.state.minItemLevel,
        max: this.$store.state.maxItemLevel,
      },
      step,
      start: [this.minIl, this.maxIl],
      margin: step,
      connect: true,
      behaviour: 'tap-drag',
      tooltips: true,
      format: {
        to: (value: number) => value,
        from: (value: string) => Number(value),
      },
      pips: {
        mode: PipsMode.Count,
        values: 6,
        stepped: true,
        density: 100,
      },
    })

    slider.on('change', this.handleUpdate)
  }

  handleUpdate(values: (number | string)[]): void {
    this.$emit('update-ilevels', values)
  }
}
</script>

<style lang="scss">
@import '~nouislider/dist/nouislider.css';
@import '../../assets/variables.scss';

.noUi-connect {
  background-color: $main-colour;
}

.filter-card {
  padding-bottom: 3.5rem;
}
</style>
