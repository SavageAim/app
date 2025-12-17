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
      <div class="divider"><i class="material-icons icon">expand_more</i> FFXIV Patch 7.4 <i class="material-icons icon">expand_more</i></div>
      <p>A new Tier, AAC Heavyweight Tier, has been added. Please ensure to update your Team to the new Tier for everything to work smoothly!</p>
      <p>
        The following new gear has been added;
        <ul>
          <li>Courtly Lover's Weapon, Armour, and Accessories - Item Level 770</li>
          <li>Runaway Trial Weapon - Item Level 775</li>
          <li>Bygone Brass Weapon, Armour, and Accessories - Item Level 780</li>
          <li>Augmented Bygone Brass Weapon, Armour, and Accessories - Item Level 790</li>
          <li>Grand Champion Armour, and Accessories - Item Level 790</li>
          <li>Grand Champion Weapon - Item Level 795</li>
        </ul>
      </p>
      <p>The default values for the Item Level filters on the BIS pages have been updated for AAC Heavyweight Tier (770 - 795).</p>
      <p>Best of luck to all progging the Tier when it drops in January!</p>
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

<style lang="scss">
</style>
