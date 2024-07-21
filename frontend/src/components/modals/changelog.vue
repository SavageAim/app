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
      <p>
        Added the following new types of Gear released in 7.05;
        <ul>
          <!-- <li>Light-heavy Armour and Accessories - Item Level 710</li> -->
        </ul>
      </p>

      <div class="divider"><i class="material-icons icon">expand_more</i> Fixes &amp; Improvements <i class="material-icons icon">expand_more</i></div>
      <p>Moved to new beta version of XIVAPI, should fix XIVGear importing!</p>
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
