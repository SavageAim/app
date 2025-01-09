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
      <div class="divider"><i class="material-icons icon">expand_more</i> Loot Solver Algorithm Improvement / Bugfix <i class="material-icons icon">expand_more</i></div>
      <p>Improved Loot Solver algorithm to handle newfound edgecase.</p>
      <p>Also fixed silly bug in the code that was introduced when fixing the previous Loot Solver bug!</p>

      <h2 class="has-text-primary subtitle">{{ version.split('.')[0] }}.2</h2>
      <div class="divider"><i class="material-icons icon">expand_more</i> Team Delete Bugfix <i class="material-icons icon">expand_more</i></div>
      <p>Quick extra push today to deliver a bugfix to a long hidden bug during Team deletion. Sorry for the inconvenience but thank you for catching it!</p>
      <p>Thankfully it wasn't an issue for deleting anything, just caused an error at the end of the endpoint call!</p>

      <h2 class="has-text-primary subtitle">{{ version.split('.')[0] }}</h2>
      <div class="divider"><i class="material-icons icon">expand_more</i> Character Verify Bugfix <i class="material-icons icon">expand_more</i></div>
      <p>Fixed a bug during the Character Verification process where it couldn't do cleanup, which first occurred yesterday.</p>
      <p>For an explanation of the bug and what was done to fix it;
        <ul>
          <li>Previously, unverified Characters could not be used to make BIS Lists or join Teams or anything, so when you verified a Character the system would delete all the unverified versions of the same Character by Lodestone ID.</li>
          <li>Now however, unverified Characters can be used for a week before everything gets deleted, but this caused a bug in the cleanup process where if an unverified version had a BIS List it couldn't be deleted.</li>
          <li>Also, any proxies using the same Character get merged into the verified Character, consolidating all BIS Lists and Team Membership into the verified Character.</li>
          <li class="has-text-primary">The fix I have implemented is to do this consolidation for un-verified Characters belonging to the same User as well, and leaving unverified versions owned by other Users to be deleted after the week deadline.</li>
        </ul>
      </p>
      <p>If anyone would like to share feedback / give ideas on this matter, please let me know on Github or in the Discord, or by using the new addition below. Hopefully this is an acceptable solution!</p>

      <div class="divider"><i class="material-icons icon">expand_more</i> Feedback Form <i class="material-icons icon">expand_more</i></div>
      <p>
        Added a little Feedback widget for another mechanism of gathering feedback for people not on Github or don't want to join the Discord.
        <ul>
          <li>I need to upgrade the website UI from using Vue 2 to Vue 3; I'm aiming to start on this in the downtime after 7.2 drops.</li>
          <li>I intend to keep the site as close as possible as how it is to use currently so if you like how it works then don't worry!</li>
          <li>However, if there are bugs/issues that I haven't caught, or if there is anything you think is weird or difficult to use, please let me know!</li>
          <li>I want to make this site as good as I can, and I want you all to be as happy as possible using it as well, so please help me if there is anything I should know!</li>
        </ul>
      </p>
      <p>I wasn't planning on releasing this so soon but I wanted the bugfix out ASAP and this was already in the codebase :D</p>
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
