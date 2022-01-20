<template>
  <div class="hero is-fullheight-with-navbar">
    <div class="hero-body">
      <div class="container has-text-centered">
        <h1 class="title is-1">
          50<span class="has-text-danger">0</span>
        </h1>
        <p class="subtitle">
          Sorry, something happened on our end. We'll look into it!
        </p>
        <router-link to="/">Go Home?</router-link>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'

@Component
export default class Error500 extends Vue {
  mounted(): void {
    document.title = 'Server Error - Savage Aim'
  }
}
</script>

<style lang="scss" scoped>
.hero {
  overflow-y: hidden;
}
</style>
