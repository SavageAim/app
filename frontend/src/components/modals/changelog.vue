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

      <div class="divider"><i class="material-icons icon">expand_more</i> Major Fixes <i class="material-icons icon">expand_more</i></div>
      <p>
        Fixed a pretty major issue with XIVAPI that prevented new Characters from being imported.
        <ul>
          <li>Unsure how long this was present, and I'm genuinely very sorry if it affected you..</li>
        </ul>
      </p>

      <div class="divider"><i class="material-icons icon">expand_more</i> Other Updates <i class="material-icons icon">expand_more</i></div>
      <p>Added more visibility into frontend errors so I can become more aware of what issues arise and when.</p>
      <p>Security updates.</p>
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
