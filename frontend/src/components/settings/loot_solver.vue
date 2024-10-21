<template>
  <div class="card">
    <div class="card-header">
      <div class="card-header-title">Loot Solver Settings</div>
    </div>
    <div class="card-content">
      <div class="field">
        <label class="checkbox">
          <input type="checkbox" :checked="lootSolverGreed" @input="changeGreed">
          Greed-y Loot Solver
        </label>
      </div>
      <div class="divider"><i class="material-icons icon">expand_more</i> Explanation <i class="material-icons icon">expand_more</i></div>
      <div class="content">
        <p>Typically, the Loot Solver Algorithm will calculate every week of loot distribution until there are no more required.</p>
        <p>However, on the final week (typically when you can buy your last items with tokens), the solver will still assign items to people who may only need one more.</p>
        <p>This removes a chance for the dropped item to go to someone's alt job BIS Lists, when the assigned player could have bought the item anyway.</p>
        <p>Turning on the Loot Solver's Greedy mode will make it stop assigning items as soon as it can, allowing those extra items to go to people faster, in exchange for more people spending their books on items.</p>
        <p>Can be toggled on/off at any time so feel free to play around with it and experiment!</p>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'
import { SettingsErrors } from '@/interfaces/responses'

@Component
export default class LootSolverSettings extends Vue {
  @Prop()
  errors!: SettingsErrors

  @Prop()
  lootSolverGreed!: boolean

  changeGreed(event: Event): void {
    const checkbox = event.target as HTMLInputElement
    const value = checkbox.checked
    this.$emit('changeLootSolverGreed', value)
  }
}
</script>
