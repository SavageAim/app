<template>
  <div class="hero is-fullheight-with-navbar">
    <div class="hero-body">
      <div class="container has-text-centered">
        <h1 class="title is-1">
          40<span class="has-text-danger">4</span>
        </h1>
        <p class="subtitle">
          All of the accuracy melds in the world can't save you now.
        </p>
        <router-link to="/">Go Home?</router-link>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'

@Component
export default class Error404 extends Vue {
  mounted(): void {
    document.title = 'Page Not Found - Savage Aim'
  }
}
</script>

<style lang="scss" scoped>
.hero {
  overflow-y: hidden;
}
</style>
