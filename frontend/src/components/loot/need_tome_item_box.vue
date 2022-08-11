<template>
  <div class="box list-item" :key="`need-${entry.member_id}`" data-microtip-position="top" role="tooltip" :aria-label="`Requires: ${entry.requires}`" >
    <span class="badge is-primary">{{ itemsReceived }}</span>
    <span class="badge is-link is-left is-hidden-desktop">{{ entry.requires }}</span>
    <div class="list-data">
      <div class="left">
        {{ entry.character_name }}
      </div>
      <div class="right">
        <div class="tags has-addons is-hidden-touch">
          <span class="tag is-light">
            Requires
          </span>
          <span class="tag is-link">
            {{ entry.requires }}
          </span>
        </div>
        <span class="icon">
          <img :src="`/job_icons/${entry.job_icon_name}.png`" :alt="`${entry.job_icon_name} job icon`" width="24" height="24" />
        </span>
      </div>
    </div>
    <div v-if="userHasPermission" class="list-actions">
      <button class="button is-success" @click="save" v-if="!requesting">Give Item</button>
      <button class="button is-success is-loading" v-else>Give Item</button>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator'
import { TomeNeedGear } from '@/interfaces/loot'

@Component
export default class NeedTomeItem extends Vue {
  @Prop()
  entry!: TomeNeedGear

  @Prop()
  itemsReceived!: number

  @Prop()
  requesting!: boolean

  @Prop()
  userHasPermission!: boolean

  save(): void {
    this.$emit('save')
  }
}
</script>

<style lang="scss">

</style>
