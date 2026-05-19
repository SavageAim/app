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
      <div class="divider"><i class="material-icons icon">expand_more</i> We're Back! <i class="material-icons icon">expand_more</i></div>
      <p>If you can see this, then we're back online!</p>
      <p>We've successfully moved host to a new provider that hopefully won't go away any time soon, and we should be better than ever on an infrastructure angle!</p>
      <p>To help cover the costs, there's a <b>COMPLETELY OPTIONAL</b> Patreon link in the footer of the page.</p>
      <p>If you feel generous enough to help cover server costs, then by all means go support the app there!</p>
      <p>There are no real benefits to it though other than the knowledge that you are doing it, but if you still want to then thank you so much!</p>
      <p>Either way, more work to do so I'll see y'all soon!</p>
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
