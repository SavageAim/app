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
        BIS List updates will now automatically swap the current ring slots if, for example, the current left ring matches the bis right ring.
        <ul>
          <li>This should hopefully make the Loot Solver / Manager break less often.</li>
          <li>This deployment has also re-saved every BIS List in the system to automatically update the lists for everyone.</li>
          <li>Thanks toonie for the suggestion!</li>
        </ul>
      </p>
      <p>Added a message to the Loot Solver that links to the Settings page if you are not using the Per-Fight Loot Manager, just in case you want to use auto-assign but don't know how.</p>
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
