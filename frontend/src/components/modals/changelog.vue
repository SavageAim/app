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
      <div class="divider"><i class="material-icons icon">expand_more</i> Navbar Changes and Improvements <i class="material-icons icon">expand_more</i></div>
      <p>The explanation for what colours mean has been moved to the Theme settings page, and removed from the navigation menu.</p>
      <p>
        The explanation for what colours mean has been moved to the Theme settings page, and removed from the navigation menu.
        <ul><li>For anyone who's usernames are different since the Discord Username update, this will probably help!</li></ul>
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
