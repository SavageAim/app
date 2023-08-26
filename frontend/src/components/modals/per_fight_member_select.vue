<template>
  <div>
    <div class="card-header">
      <div class="card-header-title">Select a recipient for {{ item }}.</div>
      <div class="card-header-icon">
        <a class="icon" @click="() => { this.$emit('close') }">
          <i class="material-icons">close</i>
        </a>
      </div>
    </div>
    <div class="card-content">
      <!-- Need Items -->
      <a class="box list-item" v-for="entry in need" :key="`need-${entry.member_id}`" data-microtip-position="top" role="tooltip" :aria-label="tome ? `Requires: ${entry.requires}` : `Current: ${entry.current_gear_name}`" >
        <span class="badge is-primary">{{ getNeedReceived(entry) }}</span>
        <span v-if="tome" class="badge is-link is-left is-hidden-desktop">{{ entry.requires }}</span>
        <div class="list-data">
          <div class="left">
            {{ entry.character_name }}
          </div>
          <div class="right">
            <div class="tags has-addons is-hidden-touch" v-if="tome">
              <span class="tag is-light">
                Requires
              </span>
              <span class="tag is-link">
                {{ entry.requires }}
              </span>
            </div>
            <div class="tags has-addons is-hidden-touch" v-else>
              <span class="tag is-light">
                iL
              </span>
              <span class="tag" :class="[`is-${entry.job_role}`]">
                {{ entry.current_gear_il }}
              </span>
            </div>
            <span class="icon">
              <img :src="`/job_icons/${entry.job_icon_name}.png`" :alt="`${entry.job_icon_name} job icon`" width="24" height="24" />
            </span>
          </div>
        </div>
      </a>

      <!-- Greed Items -->
      <GreedCharacterEntry
        v-for="entry in greed"
        :key="`greed-${entry.member_id}`"

        :items-received="getGreedReceived(entry)"
        :entry="entry"
        :raid="!tome"

        v-on:save-tome="() => {  }"
        v-on:save-raid="(list) => {  }"
      />
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'
import NeedRaidItemBox from '@/components/loot/need_raid_item_box.vue'
import NeedTomeItemBox from '@/components/loot/need_tome_item_box.vue'
import {
  GreedGear,
  LootReceived,
  NeedGear,
  TomeGreedGear,
  TomeNeedGear,
} from '@/interfaces/loot'

@Component({
  components: {
    NeedRaidItemBox,
    NeedTomeItemBox,
  },
})
export default class LoadCurrentGear extends Vue {
  @Prop()
  greed!: GreedGear[] | TomeGreedGear[]

  @Prop()
  item!: string

  @Prop()
  need!: NeedGear[] | TomeNeedGear[]

  @Prop()
  received!: LootReceived

  @Prop()
  tome!: boolean

  getGreedReceived(entry: GreedGear | TomeGreedGear): number {
    // Given an entry, return how many times that Character has received greed loot so far this tier
    return this.received[entry.character_name].greed
  }

  getNeedReceived(entry: NeedGear | TomeNeedGear): number {
    // Given an entry, return how many times that Character has received need loot so far this tier
    return this.received[entry.character_name].need
  }
}
</script>

<style lang="scss" scoped>
</style>
