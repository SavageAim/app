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
      <div class="divider"><i class="material-icons icon">expand_more</i> New Features <i class="material-icons icon">expand_more</i></div>
      <p>
        It is now possible to import your current gear from Lodestone when creating/editing BIS Lists!
        <ul>
          <li>If your current gear on Lodestone is not equippable by the Job your BIS List is set to, it will give a message and not make any changes.</li>
        </ul>
      </p>

      <div class="divider"><i class="material-icons icon">expand_more</i> Continuing UI Consistency <i class="material-icons icon">expand_more</i></div>
      <p>Colours of Action buttons in BIS List pages have been changed to a darker blue to free-up the lighter blue for specific purposes.</p>

      <div class="divider"><i class="material-icons icon">expand_more</i> Fixes & Improvements <i class="material-icons icon">expand_more</i></div>
      <p>Attempting to optimize queries on the Loot Manager page to improve performance!</p>
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
