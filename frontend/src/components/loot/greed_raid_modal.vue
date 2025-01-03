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
      <a class="box list-item" v-for="list in entry.greed_lists" :key="list.bis_list_id" data-microtip-position="top" role="tooltip" :aria-label="`Current: ${list.current_gear_name}`" @click="() => { select(list) }">
        <div class="list-data">
          <div class="left">
            {{ list.bis_list_name }}
          </div>
          <div class="right">
            <div class="tags has-addons is-hidden-touch">
              <span class="tag is-light">
                iL
              </span>
              <span class="tag" :class="[`is-${list.job_role}`]">
                {{ list.current_gear_il }}
              </span>
            </div>
            <span class="icon">
              <img :src="`/job_icons/${list.job_icon_name}.webp`" :alt="`${list.job_icon_name} job icon`" width="24" height="24" />
            </span>
          </div>
        </div>
      </a>
      <button class="button is-info is-fullwidth" @click="() => { select(null) }">Give to Character</button>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator'
import { GreedGear, GreedItem } from '@/interfaces/loot'

@Component
export default class GreedRaidModal extends Vue {
  @Prop()
  entry!: GreedGear

  @Prop()
  save!: (list: GreedItem | null) => void

  select(list: GreedItem | null): void {
    this.save(list)
    this.$emit('close')
  }
}
</script>

<style lang="scss" scoped>
</style>
