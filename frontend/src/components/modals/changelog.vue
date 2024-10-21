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
      <div class="divider"><i class="material-icons icon">expand_more</i> Loot Solver Greed-y Mode <i class="material-icons icon">expand_more</i></div>
      <p>
        Set the weeks-per-token-purchase for the second fight of a Tier to <code>3</code>, as accessory augments are only 3 tokens instead of 4.
        <ul>
          <li>This shouldn't affect the loot distrib rolls, only it now requires less weeks to get there!</li>
        </ul>
      </p>
      <p>Fixed some issues with proxy character pages not rendering properly.</p>
      <p>Fixed errors occurring when trying to import from Lodestone when the Character is missing equipment.</p>
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
