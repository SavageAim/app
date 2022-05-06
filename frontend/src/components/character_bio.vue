<template>
  <article class="media">
    <aside class="media-left">
      <figure class="image is-64x64">
        <img class="is-rounded" :src="character.avatar_url" :alt="`${character.name} Lodestone Profile Picture`" height="64" width="64">
      </figure>
    </aside>
    <div class="media-content">
      <p class="title is-4">{{ character.name }}</p>
      <div class="subtitle">
        <div class="icon-text">
          <span class="icon"><i class="material-icons">public</i></span>
          <span>{{ character.world }}</span>
        </div>
        <div class="icon-text" v-if="character.alias.length > 0">
          <span class="icon"><i class="material-icons">account_circle</i></span>
          <span>{{ character.alias }}</span>
        </div>
      </div>
    </div>
    <div v-if="displayUnverified && !character.verified" class="media-right is-hidden-mobile">
      <div class="icon has-text-danger" title="Not Verified">
        <i class="material-icons">warning</i>
      </div>
    </div>
  </article>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'
import { Character } from '@/interfaces/character'

@Component
export default class CharacterBio extends Vue {
  @Prop()
  character!: Character

  @Prop({ default: true })
  displayUnverified!: boolean
}
</script>

<style lang="scss">
.subtitle .icon-text:not(:last-child) {
  margin-bottom: 0.25rem;
}
</style>
