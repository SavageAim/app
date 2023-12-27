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
      <div class="divider"><i class="material-icons icon">auto_awesome</i> Happy Holidays and Happy New Year <i class="material-icons icon">auto_awesome</i></div>
      <p>Hard to believe I've been at this for nearly 2 years now! Hope everyone had a good end to 2023 and a nice start to 2024. Roll on Dawntrail!!</p>

      <div class="divider"><i class="material-icons icon">expand_more</i> Navigation Changes <i class="material-icons icon">expand_more</i></div>
      <p>The explanation for what colours mean has been moved to the Theme settings page, and removed from the navbar.</p>
      <p>
        A quick-switcher (similar to Discord's) has been added for faster moving between pages.
        <ul>
          <li>It's accessible through the navbar, or by pressing <code>Ctrl</code>+<code>K</code> on PC.</li>
          <li>This menu allows you to type to search for pages, and select them via arrow keys or clicking/tapping.</li>
          <li>It shows the top 5 most relevant items to your search, and when empty the list displays main character / team pages instead.</li>
        </ul>
      </p>

      <div class="divider"><i class="material-icons icon">expand_more</i> Other Fixes <i class="material-icons icon">expand_more</i></div>
      <p>If a non-leader accesses the Team's Settings page, the redirect will now put them back on the correct page.</p>

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
