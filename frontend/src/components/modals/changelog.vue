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
      <div class="divider"><i class="material-icons icon">expand_more</i> Loot Solver Greed Improvements <i class="material-icons icon">expand_more</i></div>
      <p>
        Made it so that when people have Greed BIS Lists, you can still generically assign items to them without updating one of their BIS Lists if the item is not relevant.
        <ul>
          <li>For example, currently, if a WHM weapon drops from a fourth fight, and the person who gets it has Greed BIS Lists, but none for WHM, the only way to track the item was to track it manually via the form in the History section.</li>
          <li>Now there is a generic "Give Item to Character" button even if they have Greed lists, to give them an item that a Character obtained without it being relevant to their Greed lists.</li>
        </ul>
      </p>
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
