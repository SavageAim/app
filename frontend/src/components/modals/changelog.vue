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
      <div class="divider"><i class="material-icons icon">expand_more</i> Bugfixes <i class="material-icons icon">expand_more</i></div>
      <p>
        Fixed a timezone-based bug when creating manual Loot Entries.
        <ul>
          <li>Due to the server running in UTC time, people in timezones ahead of UTC can have issues where the server will tell them that they cannot create Loot for in the future.</li>
          <li>To make it work, now the server will accept Loot for the day after its current day!</li>
        </ul>
      </p>
      <p>Fixed an issue where the mobile version of the Loot Solver would show incorrect numbers for some fields.</p>
      <p>Improved the Viper and Pictomancer icons finally!</p>
      <p>Fixed some issues in the OpenAPI schema!</p>

      <div class="divider"><i class="material-icons icon">expand_more</i> Quick-Set to BIS <i class="material-icons icon">expand_more</i></div>
      <p>Thank you Rak for the feature request!</p>
      <p>All of the Current Gear dropdowns on the Edit BIS pages now have a button you can click to instantly set the Current value to your set BIS value for that slot!</p>
      <p>This just brings a little bit of QoL to anyone updating their BIS Lists manually, after purchasing items for example!</p>
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
