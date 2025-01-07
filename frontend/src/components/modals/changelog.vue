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
      <div class="divider"><i class="material-icons icon">expand_more</i> Feedback Request <i class="material-icons icon">expand_more</i></div>
      <p>
        Hey everyone! I've added a simple feedback widget to get more opinions on how the site is to use!
        <ul>
          <li>The time is coming for quite a large rewrite of the site's code to upgrade from Vue 2 to Vue 3.</li>
          <li>I want to keep the site as close to how it is currently as possible, but I'm also using this as an opportunity to fix any major issues with how the site works for users like you!</li>
          <li>If there is anything weird or annoying or that you would like to be able to do in this future version, please let me know using the feedback form!</li>
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
