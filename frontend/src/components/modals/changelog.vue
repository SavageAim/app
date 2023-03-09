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

      <div class="divider"><i class="material-icons icon">expand_more</i> FFXIV 6.3x Patches <i class="material-icons icon">expand_more</i></div>
      <p>Added the following new gear;
        <ul>
          <li>Ultimate Omega Weapons - Item Level 635</li>
          <li>Amazing Manderville Weapons - Item Level 630</li>
        </ul>
      </p>

      <p class="has-text-primary">I'm really sorry about how long it took me to add the 6.31 patch data to the site. Have had a bit of a rough time recently but I'm back on my feet and ready to keep working on this site o7</p>

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
