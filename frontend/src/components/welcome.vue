<template>
  <div class="container">
    <div class="card">
      <div class="card-header">
        <div class="card-header-title is-centered">
          <figure class="image is-64x64">
            <img class="is-rounded" src="/materia.png" alt="Savage Aim Materia Logo" width="64" height="64" />
          </figure>
          <h2 class="title">Savage <span class="has-text-danger">Aim</span></h2>
        </div>
      </div>
      <div class="card-content has-text-centered">
        <p>Savage Aim is an online tool designed mainly for managing the Best-in-Slot (BiS) lists of Savage prog groups in FFXIV.</p>
        <p>It's built by someone who currently raids Savage blind, and therefore a lot of the features are built initially with my own requirements in mind.</p>
        <p>If you'd like to help support the development, I'd welcome suggestions and ideas and feedback!</p>
        <p>Please note we currently only support authentication through Discord, though if need be, we can add more providers soon!</p>
        <p>Happy Raiding :D</p>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'

// TODO - Make getting feedback possible, either a discord or some other thing idk
@Component
export default class Welcome extends Vue {}
</script>

<style lang="scss" scoped>
.card-header-title .title {
  font-weight: 300;
  padding-left: 1rem;
}
</style>
