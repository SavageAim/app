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
      <div class="divider"><i class="material-icons icon">expand_more</i> Import from Lodestone <i class="material-icons icon">expand_more</i></div>
      <p>The ability to import your currently equipped gear from Lodestone has been added!</p>
      <p>This only works if the currently readable version of Lodestone has gear on your character that is the same job as the one your BIS is for.</p>
      <p class="has-text-info">Please note that due to Lodestone caching, job changes on Lodestone may take a few hours to appear!</p>

      <div class="divider"><i class="material-icons icon">expand_more</i> Other Updates <i class="material-icons icon">expand_more</i></div>
      <p>Improved the database interaction for calculating required loot, so the page should now load faster!</p>
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
