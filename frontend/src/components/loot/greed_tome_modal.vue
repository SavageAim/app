<template>
  <div>
    <div class="card-header">
      <div class="card-header-title">
        Select a BIS List to get the item.
      </div>
      <div class="card-header-icon">
        <a class="icon" @click="() => { this.$emit('close') }">
          <i class="material-icons">close</i>
        </a>
      </div>
    </div>
    <div class="card-content">
      <a class="box list-item" v-for="list in entry.greed_lists" :key="list.bis_list_id" data-microtip-position="top" role="tooltip" :aria-label="`Requires: ${list.requires}`" @click="() => { select(list) }">
        <span class="badge is-link is-topleft is-hidden-desktop">{{ list.requires }}</span>
        <div class="list-data">
          <div class="left">
            {{ list.bis_list_name }}
          </div>
          <div class="right">
            <div class="tags has-addons is-hidden-touch">
              <span class="tag is-light">
                Requires
              </span>
              <span class="tag is-link">
                {{ list.requires }}
              </span>
            </div>
            <span class="icon">
              <img :src="`/job_icons/${list.job_icon_name}.png`" :alt="`${list.job_icon_name} job icon`" width="24" height="24" />
            </span>
          </div>
        </div>
      </a>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator'
import { TomeGreedGear, GreedItem } from '@/interfaces/loot'

@Component
export default class GreedTomeModal extends Vue {
  @Prop()
  entry!: TomeGreedGear

  @Prop()
  save!: (list: GreedItem) => void

  select(list: GreedItem): void {
    this.save(list)
    this.$emit('close')
  }
}
</script>

<style lang="scss" scoped>
</style>
