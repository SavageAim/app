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

      <div class="divider"><i class="material-icons icon">expand_more</i> Multiple BIS Lists per Job <i class="material-icons icon">expand_more</i></div>
      <p>The limit of one BIS List per Job has finally been removed! You can now have as many BIS Lists as you want per Job, allowing you to keep historical lists as you advance the tiers, or manage two current lists per Job for the current Tier, the options are endless!</p>
      <p>You can also give each list a name, to help differentiate different BIS Lists of the same Job. The name will default to the name of the Job.</p>
      <p>
        As part of this update, the following functionality has been changed;
        <!-- <ul>
          <li>Create / Edit BIS List pages have the ability to pull Current Gear from other BIS Lists of the same Job.</li>
          <li>Similarly, these pages also have a new second save button allowing you to save Current Gear to any other BIS List of the same Job as you choose.</li>
          <li>The Greed section of the Loot Manager page has been changed to use modals to avoid extending the page further than it has to be.</li>
          <li></li>
        </ul> -->
      </p>

      <div class="divider"><i class="material-icons icon">expand_more</i> Minor Changes <i class="material-icons icon">expand_more</i></div>
      <p>Minor changes to the breadcrumbs in the BIS Create / Edit pages.</p>
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
