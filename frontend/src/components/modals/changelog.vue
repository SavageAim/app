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
      <div class="divider"><i class="material-icons icon">expand_more</i> Major Changes <i class="material-icons icon">expand_more</i></div>
      <p>Added a settings popup under the User dropdown.</p>
      <p>Currently the only setting is to change your theme for the coloured BIS List displays on the team page and in the colours popup.</p>
      <p>However we have laid the groundwork to add more customisation in the future!</p>

      <div class="divider"><i class="material-icons icon">expand_more</i> Minor Changes <i class="material-icons icon">expand_more</i></div>
      <p>
        Changed current gear display on BIS tables in the team page to use tooltips instead of the HTML title element.
        <ul><li>This means that mobile users can now tap on slots in the tables to see a tooltip indicating the current gear in the slot.</li></ul>
      </p>
      <p>Page titles now update so your tab and history displays will have more detail to them!</p>
      <p>Any 404 errors will keep the URL used to generate them, instead of replacing it the /404.</p>
      <p>Moved the system to dedicated infrastructure!</p>
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
