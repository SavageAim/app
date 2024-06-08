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
      <div class="divider"><i class="material-icons icon">expand_more</i> API Keys <i class="material-icons icon">expand_more</i></div>
      <p>In order to allow easy access to Savage Aim from outside the website, I've added API Keys to Users.</p>
      <p>These can be generated in the User Settings page.</p>
      <p>As an example of something to use this new feature for, check out the Savage Aim Github page. Something there might catch your eye!</p>
      <p class="has-text-info">Be sure to regenerate your key if you feel like there is a chance it has been compromised!</p>

      <div class="divider"><i class="material-icons icon">expand_more</i> Fixes & Improvements <i class="material-icons icon">expand_more</i></div>
      <p>
        Improved handling for importing gear where the name on the platform is for a collection of items that have their own names.
        This should be a massive improvement for people who use the automated imports from places like Etro or the Lodestone.
        <ul>
          <li>Credendum and Augmented Credendum Weapons all have their own unique names, most of which would not have been imported as the proper Gear name previously.</li>
          <li>Artifact Gear has unique names for every job set, and the weapons typically all have their own unique names as well.</li>
        </ul>
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
