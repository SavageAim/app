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

      <div class="divider"><i class="material-icons icon">expand_more</i> Loot Manager Update <i class="material-icons icon">expand_more</i></div>
      <p>
        The "Mount", "Tome Weapon Token" and "Tome Weapon Augment" fields in the loot manager are now returned by the API.
        <ul>
          <li>They have been given naive implementation; if a team member has not yet received one, they will appear in the need list.</li>
          <li>Also, for both fields involving Tome Weapons, every member will appear in greed.</li>
          <li>Mount will never have anyone in the greed field for it as it is impossible to get a mount twice.</li>
        </ul>
      </p>
      <p>
        The colour of the "BIS Lists" tag showing how many greed lists a Character has that need an item has been changed.
        <ul>
          <li>This has been done so the dark blue is only used for the "Amount of Augment Tokens Required", for consistency across Desktop and Mobile.</li>
        </ul>
      </p>

      <div class="divider"><i class="material-icons icon">expand_more</i> Per Fight Loot Manager <i class="material-icons icon">expand_more</i></div>
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
