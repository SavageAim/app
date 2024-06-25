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
      <div class="divider"><i class="material-icons icon">expand_more</i> Dawntrail Release <i class="material-icons icon">expand_more</i></div>
      <p>Happy first new expansion for SavageAim, and a happy 7.0 to all of you wonderful gamers out there!</p>
      <p>Added two new Jobs!</p>
      <p>
        <div class="icon-text">
          <span class="icon">
            <img :src="`/job_icons/VPR.webp`" :alt="`Viper Job Icon`" width="24" height="24" />
          </span>
          <span>Viper - Melee (Scouting) DPS</span>
        </div>
        <div class="icon-text">
          <span class="icon">
            <img :src="`/job_icons/PCT.webp`" :alt="`Pictomancer Job Icon`" width="24" height="24" />
          </span>
          <span>Pictomancer - Magical Ranged DPS</span>
        </div>
      </p>
      <p>
        Added Gear associated with Dawntrail's release;
        <ul>
          <li>Level 100 Dungeon Accessories - Item Level 690</li>
          <li>Dawntrail Artefact Weapons and Armour - Item Level 690</li>
          <li>Aesthetics Tome Weapons, Armour, and Accessories - Item Level 700</li>
          <li>EX Trial Weapons and Accessories - Item Level 710</li>
        </ul>
      </p>
      <p>Names have been kept out of the changelog to avoid spoilers, so please be careful when updating your current gear to ensure you don't spoil yourself!</p>

      <div class="divider"><i class="material-icons icon">expand_more</i> API Keys <i class="material-icons icon">expand_more</i></div>
      <p>Users can now generate personal API Keys in the User Settings page.</p>
      <p>You can use these keys to access your data from outside of the website, like from our new fancy <a href="https://github.com/SavageAim/plugin" target="_blank">Dalamud plugin!</a></p>
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
