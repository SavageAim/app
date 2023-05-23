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
          <li>Diadochos Weapons, Armour, and Accessories; Item Level 640</li>
          <li>Anabaseios Armour, and Accessories; Item Level 640</li>
          <li>Voidcast Weapons; Item Level 645</li>
          <li>Credendum Weapons, Armour, and Accessories; Item Level 650</li>
          <li>Augmented Credendum Weapons, Armour, and Accessories; Item Level 660</li>
          <li>Ascension Armour, and Accessories; Item Level 660</li>
          <li>Ascension Weapons; Item Level 665</li>
        </ul>
      </p>
      <p>While the Tome weapons have their own names, they are considered Credendum for ease.</p>
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
