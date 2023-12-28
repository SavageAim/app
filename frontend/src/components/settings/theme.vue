<template>
  <div>
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
            <th class="is-il-minus-0">Max IL Gear that is not Best in Slot</th>
          </tr>
          <tr>
            <th class="is-il-minus-5">Max IL - 5 (Typically Augmented Tome Gear)</th>
          </tr>
          <tr>
            <th class="is-il-minus-10">Max IL - 10 (Typically Later Trial Weapon)</th>
          </tr>
          <tr>
            <th class="is-il-minus-15">Max IL - 15 (Typically Unaugmented Tome Gear)</th>
          </tr>
          <tr>
            <th class="is-il-minus-20">Max IL - 20 (Typically Early Catchup Trial Weapon)</th>
          </tr>
          <tr>
            <th class="is-il-minus-25">Max IL - 25 (Typically Crafted Sets)</th>
          </tr>
          <tr>
            <th class="is-il-out-of-range">Out of the range of the Team's current Tier</th>
          </tr>
        </table>
      </div>
    </div>

    <div class="card">
      <a class="card-header" @click="toggleExplanation">
        <div class="card-header-title">
          Explanation of Colours
        </div>
        <div class="card-header-icon">
          <span class="icon">
            <i class="material-icons" v-if="explanationHidden">expand_more</i>
            <i class="material-icons" v-else>expand_less</i>
          </span>
        </div>
      </a>
      <div class="card-content content" :class="{'is-hidden': explanationHidden}">
        <p>For indicating the difference between what is needed and what is currently equipped, BIS Lists are displayed with text on coloured backgrounds.</p>
        <p>
          The text in the boxes indicates the BIS item for that slot, and the colour of the box indicates the current status.
          If the current item is the same as BIS, then the box will be coloured in the colour as shown in the "Best in Slot" square above.
        </p>
        <p>
          If the current item is not BIS, then the difference in item level between the currently equipped item and the tier's maximum will determine the box's colour.
          For example, someone with Classical (iL 580) gear equipped in Asphodelos (max iL 605) will have the "Max IL - 25" colour in the box.
        </p>
        <p>
          It is also possible to hover the mouse cursor over a box to have a popup be displayed which indicates the exact type of gear equipped in the slot.
          Unfortunately this feature is not yet replicable on mobile / touchscreen devices.
        </p>
      </div>
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

  explanationHidden = true

  @Prop()
  theme!: string

  get dropdown(): HTMLSelectElement {
    return this.$refs.dropdown as HTMLSelectElement
  }

  changeTheme(): void {
    this.$emit('changeTheme', this.dropdown.value)
  }

  toggleExplanation(): void {
    this.explanationHidden = !this.explanationHidden
  }
}
</script>
