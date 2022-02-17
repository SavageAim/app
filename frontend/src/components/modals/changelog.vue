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
      <div class="divider"><i class="material-icons icon">expand_more</i> Deletion Update <i class="material-icons icon">expand_more</i></div>
      <p>Wrong / Bad / Old data getting you down? Well now you can finally get rid of it!</p>
      <p>
        <ul>
          <li>Characters and BIS Lists are deleted from the Character page. <span class="has-text-danger">BIS Lists cannot be deleted if they are used in a Team.</span></li>
          <li>Teams are disbanded through the Team Settings page.</li>
          <li>The Team Details page provides methods for Members to leave Teams, or for Team Leaders to kick Members.</li>
        </ul>
      </p>

      <div class="divider"><i class="material-icons icon">expand_more</i> Minor Changes <i class="material-icons icon">expand_more</i></div>
      <p>Improved visibility of links in card footers by making the default colour lighter, and all links bold.</p>
      <p>Changed the "Add New" links on the Dashboard to be the same style as all other card footer links, instead of being buttons.</p>
      <p>Team Details card footer links are now stored in an "Actions" dropdown due to the increasing number of them.</p>
      <p>Loot Tracker Greed Boxes will always have every Character in them, even if they don't have a BIS list, just for QoL.</p>
      <p>Security and error reporting improvements.</p>
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
