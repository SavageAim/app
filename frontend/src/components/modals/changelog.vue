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
          <li>For example, if a Mainhand weapon drops that someone gets via Greed, despite them not having a Greed list for that item, you would have to manually assign the item so as not to affect their Greed lists.</li>
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
