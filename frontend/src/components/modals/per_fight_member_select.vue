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
      <!-- Tabs -->
      <div class="tabs is-fullwidth">
        <ul>
          <li :class="{'is-active': tabs.showNeed}" @click="showNeed">
            <a>Need&nbsp;&nbsp;<span class="tag is-primary is-rounded">{{ need.length }}</span></a>
          </li>
          <li :class="{'is-active': tabs.showGreed}" @click="showGreed">
            <a>Greed&nbsp;&nbsp;<span class="tag is-info is-rounded">{{ greed.length }}</span></a>
          </li>
        </ul>
      </div>

      <!-- Need Items -->
      <template v-if="tabs.showNeed">
        <a class="box list-item" v-for="entry in need" :key="`need-${entry.member_id}`" data-microtip-position="top" role="tooltip" :aria-label="showRequires ? `Requires: ${entry.requires}` : `Current: ${entry.current_gear_name}`" >
          <span class="badge is-primary">{{ getNeedReceived(entry) }}</span>
          <!-- <span v-if="tome" class="badge is-link is-left is-hidden-desktop">{{ entry.requires }}</span> -->
          <div class="list-data">
            <div class="left">
              {{ entry.character_name }}
            </div>
            <div class="right">
              <div class="tags has-addons is-hidden-touch" v-if="showRequires">
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
      </template>

      <template v-if="tabs.showGreed">
        <!-- Greed Items -->
        <a class="box" v-for="entry in greed" :key="`greed-${entry.member_id}`" data-microtip-position="top" role="tooltip" :aria-label="`BIS Lists: ${entry.greed_lists.length}`" @click="() => { toggleGreedDropdown(entry.member_id) }">
          <div class="list-item">
            <span class="badge is-info">{{ getGreedReceived(entry) }}</span>
            <div class="list-data">
              <div class="left">
                {{ entry.character_name }}
              </div>

              <div class="right">
                <div class="tags has-addons is-hidden-touch">
                  <span class="tag is-light">
                    BIS Lists
                  </span>
                  <span class="tag is-link">
                    {{ entry.greed_lists.length }}
                  </span>
                </div>
                <!-- Dropdown button -->
                <span class="icon">
                  <i class="material-icons" v-if="!(greedDropdowns[entry.member_id] || false)">expand_more</i>
                  <i class="material-icons" v-else>expand_less</i>
                </span>
              </div>
            </div>
          </div>
          <div class="greed-list-container" v-if="greedDropdowns[entry.member_id] || false">
            <div class="list-data" v-for="list in entry.greed_lists" :key="`greed-${entry.member_id}-list-${list.bis_list_id}`">
              <div class="left">
                {{ list.job_icon_name }}
              </div>
              <div class="right">
                <span class="icon">
                  <img :src="`/job_icons/${list.job_icon_name}.png`" :alt="`${list.job_icon_name} job icon`" width="24" height="24" />
                </span>
              </div>
              <div class="list-actions">
                <button class="button is-success" >Select</button>
              </div>
            </div>

            <!-- If the member has no bis list just give a big button -->
            <button v-if="entry.greed_lists.length === 0" class="button is-success is-fullwidth">Select This Character</button>
          </div>
        </a>
      </template>
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

  greedDropdowns: { [id: number]: boolean } = {}

  @Prop()
  item!: string

  @Prop()
  need!: NeedGear[] | TomeNeedGear[]

  @Prop()
  received!: LootReceived

  tabs = {
    showNeed: true,
    showGreed: false,
  }

  get showRequires(): boolean {
    return (this.item === 'Tome Armour Augment' || this.item === 'Tome Accessory Augment')
  }

  getGreedReceived(entry: GreedGear | TomeGreedGear): number {
    // Given an entry, return how many times that Character has received greed loot so far this tier
    return this.received[entry.character_name].greed
  }

  getNeedReceived(entry: NeedGear | TomeNeedGear): number {
    // Given an entry, return how many times that Character has received need loot so far this tier
    return this.received[entry.character_name].need
  }

  showGreed(): void {
    this.tabs = { showNeed: false, showGreed: true }
  }

  showNeed(): void {
    this.tabs = { showNeed: true, showGreed: false }
  }

  toggleGreedDropdown(memberId: number): void {
    const prev = this.greedDropdowns[memberId] || false
    this.greedDropdowns[memberId] = !prev
    this.$forceUpdate()
  }
}
</script>

<style lang="scss" scoped>
.greed-list-container {
  padding-left: 1em;
  padding-right: 1em;
}
</style>
