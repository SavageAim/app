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
      <p>
        Websocket functionality has been added to the system, causing all updates to be received immediately without need of refreshing the page.
        <ul>
          <li>Any page that can be updated by a source other than the current user has this feature added, allowing for immediate feedback of other user's actions.</li>
          <li class="has-text-danger">Please note this was difficult to test and some issues may occur. Please report any issues in the Discord as best you can, thank you!</li>
        </ul>
      </p>
      <p>
        Also, the version scheme has changed going forward. Instead of SemVer the site will use dates of release!
        <ul>
          <li>More info <a href="https://wiki.savageaim.com/developer-visibility/changelog" target="_blank">here</a>.</li>
        </ul>
      </p>

      <div class="divider"><i class="material-icons icon">expand_more</i> Minor Changes <i class="material-icons icon">expand_more</i></div>
      <p>Added the External URL links to the footer of the cards in the BIS section of the Character page.</p>
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
