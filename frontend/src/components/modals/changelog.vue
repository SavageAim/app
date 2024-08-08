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
      <div class="divider"><i class="material-icons icon">expand_more</i> Loot Solver Update <i class="material-icons icon">expand_more</i></div>
      <p>Discovered a major issue with the Loot Solver algorithm being inefficient due to it being super naive.</p>
      <p>This release improves the algorithm to be more true to the "top N people get items every week".</p>
      <p>A whole writeup of the methodology is available <a href="https://github.com/orgs/SavageAim/discussions/1" target="_blank">here</a>, in case anyone wants to have a read!</p>
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
