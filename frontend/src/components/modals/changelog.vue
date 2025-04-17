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
      <div class="divider"><i class="material-icons icon">expand_more</i> Quality of Life <i class="material-icons icon">expand_more</i></div>
      <p>
        Team Leaders can now also send Lodestone Update requests via the Team Page for other Team Members, in case people are forgetting to update their BIS.
        <ul><li>Thanks toonie for the suggestion!</li></ul>
      </p>

      <div class="divider"><i class="material-icons icon">expand_more</i> Fixes <i class="material-icons icon">expand_more</i></div>
      <p>Improved error handling in the LootSolver when the Team's Tier mismatched with the BIS Lists in it.</p>
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
