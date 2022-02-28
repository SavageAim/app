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
      <p>Fixed issue where Discord usernames were not being displayed properly.</p>
      <p>
        Set the default theme to Traffic Lights as feedback indicated it was much more easily understood for new users than gradient colours.
        <span class="has-text-warning">If you've never changed your settings, your colours will now be this style. Please change your user settings to change off this!</span>
      </p>
      <p>Fixed bad wording in the 404 error page.</p>
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
