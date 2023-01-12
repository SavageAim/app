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

      <div class="divider"><i class="material-icons icon">expand_more</i> FFXIV Patch 6.3 <i class="material-icons icon">expand_more</i></div>
      <p>Added the following new gear;
        <ul>
          <li>New EX Trial Weapons - Item Level 625</li>
          <li>Hypostatic Armour - Item Level 620</li>
          <li>Augmented Rinascita Weapons, Armour and Accessories - Item Level 620</li>
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
