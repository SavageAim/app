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

      <div class="divider"><i class="material-icons icon">expand_more</i> Proxy Characters <i class="material-icons icon">expand_more</i></div>
      <p>Proxy Characters have been added!</p>
      <p>This feature allows Team Leaders to manage Characters even without the players signing up / joining a Team.</p>
      <p>Proxies can be claimed and verified by the appropriate User at a point in the future as needed as well.</p>
      <p>For all intents and purposes, these Proxies will be usable just like owned Characters, in Loot Manager and Team Details, etc.</p>
      <p>However they cannot be promoted to Team Leader since they have no owner.</p>

      <div class="divider"><i class="material-icons icon">expand_more</i> Proxy Character Verification <i class="material-icons icon">expand_more</i></div>
      <p>Whenever a Character is verified, if Proxies of the same Character exist they will now be replaced with the verified, User owned version.</p>
      <p>This allows Users to come later, claim their Character, and pick up where the Proxy was left!</p>

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
