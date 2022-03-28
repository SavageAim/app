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
      <div class="divider"><i class="material-icons icon">expand_more</i> 1.0 Release! <i class="material-icons icon">expand_more</i></div>
      <p>
        Added Websockets so pages update automatically.
        This is so if another user makes changes that affect you, the appropriate data on your side will also get updated automatically.
      </p>
      <p>This is the final feature I wanted to add before calling this 1.0.</p>
      <p>All future functionality and ideas will be driven by <b><i>you</i></b> so join the Discord if you have suggestions!</p>

      <div class="divider"><i class="material-icons icon">expand_more</i> Minor Changes <i class="material-icons icon">expand_more</i></div>
      <p>Added a <code>team_rename</code> notification to inform users if a team they are in has been renamed.</p>
      <p>Added dividers to the Notification settings section, to break up the groups of Notifications and make it more readable.</p>
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
