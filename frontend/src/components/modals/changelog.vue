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
      <p>If anyone would like to share feedback / give ideas on this matter, please let me know on Github or in the Discord. Hopefully this is an acceptable solution!</p>
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
