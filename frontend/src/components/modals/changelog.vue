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
      <div class="divider"><i class="material-icons icon">expand_more</i> Minor Changes <i class="material-icons icon">expand_more</i></div>
      <p>Loot Tracker Greed Boxes will always have every Character in them, even if they don't have a BIS list, just for QoL.</p>
      <p>Security and error reporting improvements.</p>

      <div class="divider"><i class="material-icons icon">expand_more</i> Bugfixes <i class="material-icons icon">expand_more</i></div>
      <p>Fixed an issue where Notification timestamps were not stored in UTC, causing issues for displaying them in other timezones.</p>
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
