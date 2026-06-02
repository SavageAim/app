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
      <div class="divider"><i class="material-icons icon">expand_more</i> FFXIV 7.51 <i class="material-icons icon">expand_more</i></div>
      <p>Added the Palazzo Diamond Weapons, Item Level 795, available from the new Dancing Mad Ultimate.</p>
      <p>Best of luck to all proggers!</p>

      <div class="divider"><i class="material-icons icon">expand_more</i> Minor Updates <i class="material-icons icon">expand_more</i></div>
      <p>Changed the Verification Reminder and Unverified Character Cleanup jobs from hourly to daily to save on costs.</p>
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
