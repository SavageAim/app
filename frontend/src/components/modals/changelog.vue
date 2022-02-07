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
      <h2 class="has-text-primary subtitle">{{ version }} - The First Discord Requests Release!</h2>
      <div class="divider"><i class="material-icons icon">expand_more</i> More Character Page Details  (from @Rai) <i class="material-icons icon">expand_more</i></div>
      <p>Split the Character page into two sections, one for BIS Lists and one for Teams.</p>
      <p>
        With only one visible at a time, the Character page can now display more information;
        <ul>
          <li>BIS Lists now display as tables similar to Team Details. <span class="has-text-warning">Uses the bis mainhand item level for colours.</span></li>
          <li>Teams now display the exact same as they do on the home page, with jobs displayed along the bottom.</li>
        </ul>
      </p>

      <div class="divider"><i class="material-icons icon">expand_more</i> Tome Augment Manager (from @Brandon) <i class="material-icons icon">expand_more</i></div>
      <p>Adds Tome Armour Augment and Tome Accessory Augment to the automated section of the Loot Manager.</p>
      <p>Due to the nature of the items in question, giving these items as loot using the manager does not update the corresponding BIS List.</p>
      <p>The boxes indicating character details for these items are differ slightly from those for the raid gear, so please check the wiki if there are any questions!</p>

      <div class="divider"><i class="material-icons icon">expand_more</i> Improve BIS Form on Mobile (from @Yord) <i class="material-icons icon">expand_more</i></div>
      <p>
        Improved User experience when creating and editing BIS Lists on mobile devices.
        <ul>
          <li>On mobile, the sections are separated into tabs to keep the page tidy and logically break up each piece of the form.</li>
        </ul>
      </p>

      <div class="divider"><i class="material-icons icon">expand_more</i> Minor Changes <i class="material-icons icon">expand_more</i></div>
      <p>Added the arbitrary loot tracking form to mobile view as well as desktop, to not keep functionality away from the mobile version.</p>
      <p>
        Using a Discord logo for the Discord link in the footer, to make it more immediately obvious what it is.
        <ul>
          <li>Note that to stick to Discord's branding guidelines, the links in the footer have all been made white when unhovered instead of the original dark blue.</li>
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
