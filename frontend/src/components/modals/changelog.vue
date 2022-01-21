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
      <p>We have a wiki now!</p>
      <p><a href="https://wiki.savageaim.com" target="_blank">wiki.savageaim.com</a></p>
      <p>Removed a lot of the help text from the pages since it's all in the wiki now!</p>

      <div class="divider"><i class="material-icons icon">expand_more</i> Minor Changes <i class="material-icons icon">expand_more</i></div>
      <p>Prevented any issues forming from Teams or Characters generating duplicate tokens by preventing that from happening altogether.</p>
      <p>Added wiki and github links to the footer.</p>
      <p>Footer now also displays the current version.</p>
      <p>Footer links now use tooltips instead of titles.</p>
      <p>BIS List form filters no longer exclude currently chosen items if their item levels are outside the range of the chosen filter values.</p>
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
