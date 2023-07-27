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

      <div class="divider"><i class="material-icons icon">expand_more</i> Updates <i class="material-icons icon">expand_more</i></div>
      <p>Wrote a new algorithm for fetching information for the Loot Manager page.</p>
      <p>Until the new Loot Manager update comes out sometime next month, I've set up the Loot Manager to randomly use either of the algorithms (50/50 split).</p>
      <p>The new one appears to be faster and less demanding in my own testing, but this kind of thing is best tested with real data.</p>
      <p>As always, if there are any issues, please report them on the Discord!</p>

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
