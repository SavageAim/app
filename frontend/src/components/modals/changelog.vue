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
      <div class="divider"><i class="material-icons icon">expand_more</i> UI Changes <i class="material-icons icon">expand_more</i></div>
      <p>
        A bunch of changes have been made to the UI of the site after some feedback.
        <ul>
          <li>The actions below a Team Member's card will now be rendered directly on the card on Desktop size displays. No more dropdown on Desktop. Icons have also been added to each link to make them stand out.</li>
          <li>Actions below BIS Lists on a Character page now also have icons, and have been consolidated under an Actions dropdown on smaller screens for consistency with the Team Member cards.</li>
          <li>Removed padding under BIS List tables for consistent spacing within their cards. Also replaced the large shadow below the header on all cards with a simple border.</li>
          <li>Added icons to most buttons/links. Buttons/links that do similar things will have the same icons, to increase visual consistency.</li>
          <li>Similarly, links and buttons with the same idea will now also be coloured the same.</li>
          <li>The Add New links on the Dashboard have been turned into buttons for more visual consistency.</li>
          <li>The buttons on the Create Proxy page have been flipped as Delete buttons tend to be on the right on this site. Also, the style has been brought in line with other similar pages.</li>
        </ul>
      </p>
      <p class="has-text-info">Feedback on these changes would be helpful also, as I want to make the best site I can!</p>

      <div class="divider"><i class="material-icons icon">expand_more</i> Other Changes <i class="material-icons icon">expand_more</i></div>
      <p>Importing from Etro now populates the BIS List's name field, if it does not already have one.</p>
      <p>Added an action under BIS Lists on a Character's page to create a copy of the BIS List.</p>
      <p>Updated the welcome page message for the first time since the site's release.</p>

      <div class="divider"><i class="material-icons icon">expand_more</i> Fixes <i class="material-icons icon">expand_more</i></div>
      <p>The heart from the Kofi logo will no longer be visible on top of dropdowns / tooltips.</p>
      <p>Tabs with errors are correctly shown in the Settings page.</p>
      <p>Errors on the Settings page are now cleared when a save is successful.</p>

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
