<template>
  <div>
    <div class="card-header">
      <div class="card-header-title">
        Changelog
      </div>
      <div class="card-header-icon">
        <a @click="() => { this.$emit('close') }" class="icon">
          <i class="material-icons">close</i>
        </a>
      </div>
    </div>
    <div class="card-content content">
      <h2 class="has-text-primary subtitle">{{ version }}</h2>

      <div class="divider"><i class="material-icons icon">expand_more</i> FFXIV Patch 6.2 Content <i class="material-icons icon">expand_more</i></div>
      <p>A new Tier, Pandæmonium: Abyssos, has been added. Please ensure to update your Team to the new Tier to have BIS Table colours display correctly!</p>
      <p>
        All the gear added with Patch 6.2 has been added to the site, please enjoy updating your BIS Lists for the new Tier!
        <ul>
          <li>Crafted Weapon, Armour and Accessories (iL 610)</li>
          <li>
            ????? Trial Weapon (iL 615)<br />
            <span class="has-text-warning">(correct name used in database so be careful re: spoilers)</span>
          </li>
          <li>Moonshine and Augmented Moonshine Tome Weapon, Armour and Accessories (iL 620 / 630)</li>
          <li>Abyssos Weapon, Armour and Accessories (iL 630 / 635)</li>
        </ul>
      </p>
      <p>The default values for the Item Level filters in BIS pages have been updated to the new range for Abyssos. (610 - 635)</p>

    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'

@Component
export default class Changelog extends Vue {
  get version(): string {
    return this.$store.state.version
  }
}
</script>
