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

      <div class="divider"><i class="material-icons icon">expand_more</i> FFXIV 6.51 Update <i class="material-icons icon">expand_more</i></div>
      <p>
        Added the following new types of Gear released in 6.51;
        <ul>
          <li>Exquisite Credendum Weapons - Item Level 665</li>
          <li>These are upgrades to Augmented Credendum Tome Weapons, obtained through Savage Criterion</li>
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
