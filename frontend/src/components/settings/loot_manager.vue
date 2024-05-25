<template>
  <div class="card">
    <div class="card-header">
      <div class="card-header-title">Loot Manager Version</div>
    </div>
    <div class="card-content">
      <div class="field">
        <div class="control">
          <div class="select is-fullwidth">
            <select :value="lootManagerVersion" @input="changeLootManagerVersion" ref="dropdown">
              <option value="item">Per Item (Original)</option>
              <option value="fight">Per Fight (Beta)</option>
            </select>
          </div>
          <p class="help is-danger" v-if="errors.loot_manager_version !== undefined">{{ errors.loot_manager_version[0] }}</p>
        </div>
      </div>
      <div class="divider"><i class="material-icons icon">expand_more</i> Example <i class="material-icons icon">expand_more</i></div>
      <template v-if="lootManagerVersion === 'item'">
        <img src="/per_item_loot_mngr.webp" alt="An example of the per item based loot manager" />
        <hr />
        <p>The original version of the Loot Manager page which works one item at a time.</p>
        <p>Back when SavageAim was initially developed, loot was dropped randomly per fight. This meant you couldn't know what items to expect until a fight was killed.</p>
        <p>As a result, this "one item at a time" method made the most sense.</p>
      </template>
      <template v-if="lootManagerVersion === 'fight'">
        <img src="/per_fight_loot_mngr.webpp" alt="An example of the per item based loot manager" />
        <hr />
        <p>A new version of the Loot Manager that leverages the changes brought to savage loot in Pandæmonium: Anabaseios.</p>
        <p>Since fights can be expected to drop one of all of their potential drops every kill, it's possible to assign all the loot per fight in one go.</p>
        <p>This is, of course, only true as long as future tiers maintain this pattern (which I really hope they do!).</p>
        <p class="has-text-info">This format is currently in beta, if you find any issues please report them on the Discord!</p>
      </template>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'
import { SettingsErrors } from '@/interfaces/responses'

@Component
export default class LootManagerSettings extends Vue {
  @Prop()
  errors!: SettingsErrors

  @Prop()
  lootManagerVersion!: string

  get dropdown(): HTMLSelectElement {
    return this.$refs.dropdown as HTMLSelectElement
  }

  changeLootManagerVersion(): void {
    this.$emit('changeLootManagerVersion', this.dropdown.value)
  }
}
</script>
