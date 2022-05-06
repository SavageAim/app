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
        Added a field for Characters to have aliases, alternative names they can go by.
        <ul>
          <li>This is accessible in the Character page, under the View Settings tab!</li>
        </ul>
      </p>
      <div class="divider"><i class="material-icons icon">expand_more</i> Minor Changes <i class="material-icons icon">expand_more</i></div>
      <p>Fixing performance issues found by some online performance checking tools.</p>
      <p>Preventing random navigation errors in vue router code.</p>
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
