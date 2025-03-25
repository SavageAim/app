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
      <div class="divider"><i class="material-icons icon">expand_more</i> FFXIV Patch 7.2 <i class="material-icons icon">expand_more</i></div>
      <p>A new Tier, AAC Cruiserweight Tier, has been added. Please ensure to update your Team to the new Tier to have BIS Table colours display correctly, and best of luck!</p>
      <p>
        All the gear added with Patch 7.2 has been added to the site, please enjoy updating your BIS Lists for the new Tier!
        <ul>
          <li>Ceremonial Weapon, Armour and Accessories - Item Level 740</li>
          <li>Cruiser Armour and Accessories - Item Level 740</li>
          <li>????? Trial Weapon - Item Level 745 (name hidden in changelog for spoilers sake)</li>
          <li>Historia Weapon, Armour and Accessories - Item Level 750</li>
          <li>Augmented Historia Weapon, Armour and Accessories - Item Level 760</li>
          <li>Babyface Champion Armour and Accessories - Item Level 760</li>
          <li>Babyface Champion Weapon - Item Level 765</li>
        </ul>
      </p>
      <p>The default values for the Item Level filters in BIS pages have been updated to the new range for Cruiserweight. (740 - 765)</p>

      <div class="divider"><i class="material-icons icon">expand_more</i> Loot Solver Bugfixes <i class="material-icons icon">expand_more</i></div>
      <p>
        Fixed a bug where the Loot Solver would assume that you could buy armour pieces from 2nd and 3rd fights of a Tier with the same number of clear-tokens as the tome augmentation items.
        <ul>
          <li>As a reminder, the Solver assumes you only buy Tome Augmentation items from the 2nd and 3rd fights!</li>
        </ul>
      </p>
      <p>Also fixed some other very well hidden bugs, so thank you to everyone for using the Loot page and giving me good data!</p>

      <div class="divider"><i class="material-icons icon">expand_more</i> Work Commencing on SavageAim "v2" <i class="material-icons icon">expand_more</i></div>
      <p>As mentioned before, I need to update some frontend libraries that the site uses for security and updates sakes.</p>
      <p>If you have any issues with the site, now is definitely the time to make them known, as I'll be trying to fix a bunch of things while keeping the site looking as much the same as possible!</p>
      <p>Leave your feedback either in the Discord (link at the bottom of the page) or using the nice lil feedback widget at the bottom right of your page!</p>
      <p>You can track v2 plans at the GitHub Issue <a href="https://github.com/SavageAim/app/issues/92" target="_blank">here!</a></p>
      <p>Thank you all for your continued support, SavageAim wouldn't be half the tool it is without y'all!</p>
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

<style lang="scss">
</style>
