<template>
  <div class="box greed-box">
    <span class="badge is-info">{{ itemsReceived }}</span>
    <div class="list-item" v-for="list in entry.greed_lists" :key="`greed-${entry.member_id}-${list.bis_list_id}`" data-microtip-position="top" role="tooltip" :aria-label="`Current: ${list.current_gear_name}`">
      <div class="list-data">
        <div class="left">
          {{ entry.character_name }}
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
            <img :src="`/job_icons/${list.job_icon_name}.png`" :alt="`${list.job_icon_name} job icon`" />
          </span>
        </div>
      </div>
      <div v-if="editable" class="list-actions">
        <button class="button is-success" @click="() => { save(list) }" v-if="!requesting">Give Item</button>
        <button class="button is-success is-loading" v-else>Give Item</button>
      </div>
    </div>

    <div class="list-item" v-if="entry.greed_lists.length === 0">
      <div class="list-data">
        <div class="left">
          {{ entry.character_name }}
        </div>
      </div>
      <div v-if="editable" class="list-actions">
        <button class="button is-success" @click="() => { save(null) }" v-if="!requesting">Give Item</button>
        <button class="button is-success is-loading" v-else>Give Item</button>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator'
import { GreedGear, GreedItem } from '@/interfaces/loot'

@Component
export default class GreedRaidItemBox extends Vue {
  @Prop()
  editable!: boolean

  @Prop()
  entry!: GreedGear

  @Prop()
  itemsReceived!: number

  @Prop()
  requesting!: boolean

  save(list: GreedItem): void {
    this.$emit('save', list)
  }
}
</script>

<style lang="scss">

</style>
