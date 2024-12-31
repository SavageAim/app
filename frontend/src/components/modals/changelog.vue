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
      <div class="divider"><i class="material-icons icon">expand_more</i> Bugfixes <i class="material-icons icon">expand_more</i></div>
      <p>Worked out some edgecase issues with the Loot Solver. If you run into any weirdness with your Team's Loot Solver, please let me know!</p>

      <div class="divider"><i class="material-icons icon">expand_more</i> Developer QoL <i class="material-icons icon">expand_more</i></div>
      <p>Ever wanted to try running SavageAim locally and messing around with it? Well the README in the GitHub repo just got a whole lot more helpful, and there's now even a command to setup your local database automatically!</p>
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
