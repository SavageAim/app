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
      <div class="divider"><i class="material-icons icon">expand_more</i> Major Changes <i class="material-icons icon">expand_more</i></div>
      <p>
        Added a new "Update" button on Character pages to refresh Character data from the Lodestone.
        <ul>
          <li>This allows Characters who have moved worlds or changed names to have the current information on Savage Aim.</li>
        </ul>
      </p>

      <div class="divider"><i class="material-icons icon">expand_more</i> Minor Changes <i class="material-icons icon">expand_more</i></div>
      <p>Fixed some under-the-hood errors that may have had minor effects on the website.</p>

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
