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
      <p>
        It is now possible to import your current gear from Lodestone when creating/editing BIS Lists!
        <ul>
          <li>If your current gear on Lodestone is not equippable by the Job your BIS List is set to, it will give a message and not make any changes.</li>
        </ul>
      </p>

      <div class="divider"><i class="material-icons icon">expand_more</i> Loot Manager - Solver <i class="material-icons icon">expand_more</i></div>
      <p>A new BETA feature has been added to the Loot Manager page; the Loot Solver.</p>
      <p>This feature aims to "solve" loot distibution by handing out loot fairly but in a way that ensures you spend the least number of weeks on each fight as possible.</p>
      <p>It is accessible in a dropdown box on the Loot Manager page, and you can see a full set of distribution for all of the required kills.</p>
      <p>People using the Per-Fight Loot Manager (accessible in User Settings) can also auto-assign the week's loot into the slots, allowing for an easy save if you're following it.</p>
      <p class="has-text-info">For more details, please see <a href="https://wiki.savageaim.com/teams/loot-manager/loot-solver" target="_blank">the wiki page</a> about this feature!</p>

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
