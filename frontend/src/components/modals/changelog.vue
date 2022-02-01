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
      <p>Notifications System has been added!</p>
      <p>
        The following events will give you notifications;
        <ul>
          <li>Character Verify requests failed or succeeded.</li>
          <li>Your Character has been put in charge of a Team it is in.</li>
          <li>Someone has joined a Team you lead.</li>
          <li>The Loot Tracker of a Team has updated one of your BIS Lists.</li>
        </ul>
      </p>
      <p>These are all toggleable, so you can disable any notification types you don't want to receive by visiting the Settings page!</p>
      <p>Currently the Notification system is polled every 30 seconds for updates, but I intend to make this truly live in the near future with instant updates when necessary!</p>

      <div class="divider"><i class="material-icons icon">expand_more</i> Minor Changes <i class="material-icons icon">expand_more</i></div>
      <p>Added Trans Pride colour scheme.</p>
      <p>Fixed issues causing too much side padding on some pages, especially on mobile views.</p>
      <p>Fixed breadcrumbs for Edit and New BIS pages linking to the wrong URL.</p>
      <p>Removed mentions of "Raid Lead", only using "Team Lead" to avoid any confusion.</p>
      <p>Add Badges to Character cards on the Loot Tracker pages to indicate how much Loot they have already received in this Tier.</p>
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
