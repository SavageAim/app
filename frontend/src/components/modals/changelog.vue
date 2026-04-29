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
      <div class="divider"><i class="material-icons icon">expand_more</i> FFXIV Patch 7.5 <i class="material-icons icon">expand_more</i></div>
      <p>
        The following new gear has been added;
        <ul>
          <li>Augmented Courtly Lover's Weapon, Armour, and Accessories - Item Level 780</li>
          <li>of Naught Trial Weapons - Item Level 785</li>
          <li>Vana'dielian Armour - Item Level 780</li>
        </ul>
      </p>
      <div class="divider"><i class="material-icons icon">expand_more</i> Potential Lodestone Import Issues <i class="material-icons icon">expand_more</i></div>
      <p>Lodestone has changed how they handle your current equipment on the website.</p>
      <p>I caught the issue before pushing this version, and updated the scraper accordingly, but they could still change it further.</p>
      <p>If there are any errors importing your Gear from Lodestone, I should be notified and will look into it asap, but I'm letting you know here in advance just in case!</p>

      <div class="divider"><i class="material-icons icon">expand_more</i> Note <i class="material-icons icon">expand_more</i></div>
      <p>I've taken a break from FFXIV recently, and as a result the site has missed a few patches of gear and such.</p>
      <p>I've added a system in the background to keep me updated when patches happen so even while I'm away I can update the site accordingly.</p>
      <p>I'm very sorry for the lull in support and updates while I've been away, I hope to be back come Evercold for the new expansion!</p>
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
