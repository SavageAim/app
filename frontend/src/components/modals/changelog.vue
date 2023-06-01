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

      <div class="divider"><i class="material-icons icon">expand_more</i> Minor Updates <i class="material-icons icon">expand_more</i></div>
      <p>Item Level filtering in BIS pages now uses a slider instead of two large dropdowns.</p>

      <div class="divider"><i class="material-icons icon">expand_more</i> Fixes <i class="material-icons icon">expand_more</i></div>
      <p>Set the default Item Level filters on BIS pages to be the item level range for Anabaseios.</p>

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
