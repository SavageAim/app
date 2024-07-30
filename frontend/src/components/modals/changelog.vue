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
      <div class="divider"><i class="material-icons icon">expand_more</i> FFXIV 7.05 Update <i class="material-icons icon">expand_more</i></div>
      <p>The newest Tier, <code>AAC Light-heavyweight Tier</code>, has begun!</p>
      <p>Please be sure to update your Team to be on this new Tier, and best of luck to everyone with your prog!! :D</p>
      <p>
        Added the following new types of Gear released in 7.05;
        <ul>
          <li>Archeo Kingdom Weapons, Armour, and Accessories - Item Level 710</li>
          <li>Quetzalli Weapons, Armour, and Accessories - Item Level 720</li>
          <li>Augmented Quetzalli Weapons, Armour, and Accessories - Item Level 730</li>
          <li>Dark Horse Champion Armour, and Accessories - Item Level 730</li>
          <li>Dark Horse Champion Weapons - Item Level 735</li>
        </ul>
      </p>

      <div class="divider"><i class="material-icons icon">expand_more</i> Fixes &amp; Improvements <i class="material-icons icon">expand_more</i></div>
      <p>Moved to using the beta version of XIVAPI, should fix XIVGear importing!</p>
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
