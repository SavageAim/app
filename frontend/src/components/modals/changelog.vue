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
      <div class="divider"><i class="material-icons icon">expand_more</i> Minor Changes <i class="material-icons icon">expand_more</i></div>
      <p>
        Fixed issue in Loot Tracker where giving a Mainhand item to a non-PLD wouldn't internally update their offhand, causing desync of information.
        <ul><li class="has-text-warning">If you have been assigned a mainhand using a Loot Tracker, go and manually save the BIS List again, which should fix this desync.</li></ul>
      </p>
      <p>Fixed issue causing random scrolls to top of page when interacting with some elements.</p>
      <p>Fixed issue where having exactly 4 latest notifications displays none of them in the latest box.</p>
      <p>Fixed issue where Job Icon is not kept updated in the new mobile version of the BIS List form.</p>
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
