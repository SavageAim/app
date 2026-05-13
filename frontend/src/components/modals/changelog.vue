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
      <div class="divider"><i class="material-icons icon">expand_more</i> Important Announcement <i class="material-icons icon">expand_more</i></div>
      <p>The hosting I've been using to provide this website is sadly closing down.</p>
      <p>This does not mean the end of the site, I will be moving the site to a different host, but sadly it won't be free like my old hosting.</p>
      <p>There will be some downtime on the site to make sure I don't lose data in the transfer.</p>
      <p>This downtime will begin Tuesday May 19th, and I aim to have everything back up and running by the end of May with no data loss.</p>
      <p>Very sorry for the inconvenience but I need to do it sooner rather than later!</p>
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
