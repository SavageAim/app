<template>
  <div class="card">
    <div class="card-header">
      <div class="card-header-title">Colour Scheme</div>
    </div>
    <div class="card-content">
      <div class="field">
        <div class="control">
          <div class="select is-fullwidth">
            <select :value="theme" @input="changeTheme" ref="dropdown">
              <option value="beta">Beta</option>
              <option value="blue">Blue</option>
              <option value="fflogs">FFLogs</option>
              <option value="green">Green</option>
              <option value="purple">Purple</option>
              <option value="red">Red</option>
              <option value="traffic">Traffic Lights</option>
              <option disabled>----- Pride Flag Schemes -----</option>
              <option value="ace">Asexual</option>
              <option value="lesbian">Lesbian</option>
              <option value="nb">Nonbinary</option>
              <option value="pan">Pan</option>
              <option value="rainbow">Rainbow</option>
              <option value="trans">Trans</option>
            </select>
          </div>
          <p class="help is-danger" v-if="errors.theme !== undefined">{{ errors.theme[0] }}</p>
        </div>
      </div>
      <div class="divider"><i class="material-icons icon">expand_more</i> Example <i class="material-icons icon">expand_more</i></div>
      <table class="table is-bordered is-fullwidth gear-table" :class="[`is-${theme}`]">
        <tr>
          <th class="is-il-bis">Best in Slot</th>
        </tr>
        <tr>
          <th class="is-il-minus-0">Max IL - 0</th>
        </tr>
        <tr>
          <th class="is-il-minus-5">Max IL - 5</th>
        </tr>
        <tr>
          <th class="is-il-minus-10">Max IL - 10</th>
        </tr>
        <tr>
          <th class="is-il-minus-15">Max IL - 15</th>
        </tr>
        <tr>
          <th class="is-il-minus-20">Max IL - 20</th>
        </tr>
        <tr>
          <th class="is-il-minus-25">Max IL - 25</th>
        </tr>
        <tr>
          <th class="is-il-out-of-range">Out of the range of the Team's current Tier</th>
        </tr>
      </table>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'
import { SettingsErrors } from '@/interfaces/responses'

@Component
export default class ThemeSettings extends Vue {
  @Prop()
  errors!: SettingsErrors

  @Prop()
  theme!: string

  get dropdown(): HTMLSelectElement {
    return this.$refs.dropdown as HTMLSelectElement
  }

  changeTheme(): void {
    this.$emit('changeTheme', this.dropdown.value)
  }
}
</script>
