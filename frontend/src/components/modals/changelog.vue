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
      <div class="divider"><i class="material-icons icon">expand_more</i> Fixes <i class="material-icons icon">expand_more</i></div>
      <p>Improved the handling of edge-case authentication issues, capturing information and redirecting back to the login page with (hopefully) helpful text on what happened.</p>
      <p>I'll keep looking into how to improve the authentication flow to make sure things like this happen less often, but sometimes errors just happen.</p>
      <p>This minor change should at least hopefully help explain what is going on and not just give people a white empty page with "Server Error (500)" written on it...</p>

      <div class="divider"><i class="material-icons icon">expand_more</i> Quality of Life <i class="material-icons icon">expand_more</i></div>
      <p>Increased login session time to 30 days instead of 14, so you don't have to log in as frequently.</p>
      <p>A long time ago I added an update about refreshing discord tokens but was confused why it wasn't helping stay logged in longer.</p>
      <p>Turns out, the sessions were defaulting to lasting 14 days.</p>
      <p>If this causes any issues, I'll fix it asap!</p>
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
