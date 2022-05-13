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
      <div class="divider"><i class="material-icons icon">expand_more</i> FFXIV 6.1.1 <i class="material-icons icon">expand_more</i></div>
      <p>
        Added the following Gear for the release of 6.1.1;
        <ul>
          <li>Ultimate of the Heavens; Item Level 605 Weapons</li>
        </ul>
      </p>

      <div class="divider"><i class="material-icons icon">expand_more</i> Massive BIS Lists Updates <i class="material-icons icon">expand_more</i></div>
      <p>The limit of one BIS List per Job has finally been removed! You can now have as many BIS Lists as you want per Job, allowing you to keep historical lists as you advance the tiers, or manage two current lists per Job for the current Tier, the options are endless!</p>
      <p>You can also give each list a name, to help differentiate different BIS Lists of the same Job. The name will default to the name of the Job.</p>
      <p>
        Syncing Current Gear between BIS Lists of the same Job is also possible, in both directions.
        <ul>
          <li>When saving a BIS List you have the option to save the Current Gear to other BIS Lists of the same Job.</li>
          <li>When creating / editing a BIS List you also have the option to pull Current Gear from another List of the same Job.</li>
        </ul>
      </p>
      <p>
        It is also now possible to import BIS Gear from Etro Gearsets by filling in the Extra URL of a BIS List.
        <ul>
          <li class="has-text-warning">Imports may not be perfect as to avoid maintaining a map for different names in the website, it compares names of Gear between Savage Aim and Etro and chooses the closest name.</li>
        </ul>
      </p>

      <div class="divider"><i class="material-icons icon">expand_more</i> Minor Changes <i class="material-icons icon">expand_more</i></div>
      <p>Minor changes to the breadcrumbs in the BIS Create / Edit pages.</p>
      <p>The Greed section of the Loot Manager page now uses popups for Characters with more than one BIS List.</p>
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
