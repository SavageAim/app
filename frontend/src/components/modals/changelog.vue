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
      <p>Fixed a bug with background tasks (like character verification) that were failing to be started properly.</p>

      <div class="divider"><i class="material-icons icon">expand_more</i> Random Authentication Failures <i class="material-icons icon">expand_more</i></div>
      <p>If you can log in but are randomly getting 403 errors when trying to do things, please <b>Reset your Cookies for this site.</b></p>
      <p>This is a leftover issue from the back-to-back migrations and only potentially affects anyone who logged in before the second migration finished on July 6th, 2026</p>
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
