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
      <p>A new settings block has been added to the Settings page for managing the Loot Solver!</p>
      <p>A more Greed-y mode has been added as a setting to the Loot Solver, which will increase the amount of items that are available for alt Jobs but also increase the amount of people who will be expected to buy their required items with tokens.</p>
      <p>This feature was requested by @Rai, hopefully this works to your liking!</p>

      <div class="divider"><i class="material-icons icon">expand_more</i> Loot Solver Bug Updates <i class="material-icons icon">expand_more</i></div>
      <p>If you have been having issues with the Loot Manager page giving you Internal Server Error messages or anything of the like, I am looking into it!</p>
      <p>This release contains some code that should help me track down the root of the error and make it reproduceable in tests, after which I will be able to catch it properly and remove it for good.</p>
      <p>I appreciate your patience as I try to uncover the root cause of this bug, thank you :D</p>
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
