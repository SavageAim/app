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

      <div class="divider"><i class="material-icons icon">expand_more</i> Settings Page Cleanup <i class="material-icons icon">expand_more</i></div>
      <p>The <router-link to="/settings/">settings page</router-link> has been expanded with extra settings.</p>
      <p>In the interest of keeping it neat, the settings sections are now accessible in separate sections, similar to the character pages.</p>
      <p>Navbar items will display an asterisk when they have been changed, to help indicate unsaved changes have been made.</p>

      <div class="divider"><i class="material-icons icon">expand_more</i> Loot Manager Version 2 <i class="material-icons icon">expand_more</i></div>
      <p>A new version of the Loot Manager has been released in beta.</p>
      <p>To view the differences, or opt in to try it out, please visit <router-link to="/settings/">your settings</router-link>.</p>
      <p class="has-text-primary">If you have any feedback, please make it known in the <a href="https://discord.gg/k8szJ5qAKw" target="_blank">Discord server</a>!</p>
      <p>Also note that the Loot Manager version is a personal setting, as both will be supported going forward.</p>

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
