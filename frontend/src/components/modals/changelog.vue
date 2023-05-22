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

      <div class="divider"><i class="material-icons icon">expand_more</i> FFXIV Patch 6.4 <i class="material-icons icon">expand_more</i></div>
      <p>Added new tier: <span class="has-text-primary">Pandæmonium: Anabaseios</span>. Team Leaders be sure to update your Team for proper BIS tracking!</p>

      <p>
        Added the following gear;
        <ul>
          <li>Crafted Weapons, Armour, and Accessories; Item Level 640</li>
          <li>Normal Mode Armour, and Accessories; Item Level 640</li>
          <li>Voidcast Dais Weapons; Item Level 645</li>
          <li>Tome Weapons, Armour, and Accessories; Item Level 650</li>
          <li>Augmented Tome Weapons, Armour, and Accessories; Item Level 660</li>
          <li>Savage Armour, and Accessories; Item Level 660</li>
          <li>Savage Weapons; Item Level 665</li>
        </ul>
      </p>
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
