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
      <h2 class="has-text-primary subtitle">{{ version }} - The First Major Release!</h2>
      <div class="divider"><i class="material-icons icon">expand_more</i> Major Changes <i class="material-icons icon">expand_more</i></div>
      <p>Websocket functionality has been added to the system, causing all updates to be received immediately without need of refreshing the page.</p>
      <p>Any page that can be updated by a source other than the current user has this feature added, allowing for immediate feedback of other user's actions.</p>
      <p>Also, the version scheme has changed going forward, and now uses the current date as the version instead of the SemVer pattern that was used previously!</p>

      <div class="divider"><i class="material-icons icon">expand_more</i> Minor Changes <i class="material-icons icon">expand_more</i></div>
      <p>Added the External URL links to BIS displays in Character pages.</p>
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
