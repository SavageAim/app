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
      <div class="divider"><i class="material-icons icon">expand_more</i> Team Permissions <i class="material-icons icon">expand_more</i></div>
      <p>Added the ability for Team Leaders to extend certain permissions to other Members of the Team.</p>
      <p>
        The permissions currently available are as follows;
        <ul>
          <li>Handing out / Tracking Loot in the Loot Manager page.</li>
        </ul>
      </p>
      <p>Permissions are editable by Team Leaders and viewable by Team Members in the new Management page.</p>
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
