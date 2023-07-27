<template>
  <div class="columns is-desktop is-multiline">
    <div class="column is-full">
      <div class="card">
        <div class="card-header">
          <div class="card-header-title">
            Select an Item
          </div>
        </div>
        <div class="card-content">
          <ItemDropdown v-model="displayItem" />

          <!-- Display generic errors here -->
          <div class="box has-background-danger" v-if="errors.greed !== undefined">
            <b>Greed: </b> {{ errors.greed[0] }}
          </div>
          <div class="box has-background-danger" v-if="errors.greed_bis_id !== undefined">
            <b>Greed BIS ID:</b> {{ errors.greed_bis_id[0] }}
          </div>
          <div class="box has-background-danger" v-if="errors.item !== undefined">
            <b>Item: </b> {{ errors.item[0] }}
          </div>
          <div class="box has-background-danger" v-if="errors.member_id !== undefined">
            <b>Member ID:</b> {{ errors.member_id[0] }}
          </div>
        </div>
      </div>
    </div>

    <!-- Need -->
    <div class="column is-half">
      <div class="card">
        <div class="card-header">
          <div class="card-header-title">
            Need
          </div>
        </div>
        <div class="card-content">
          <p>Below are the people that need the chosen item for their Team BIS.</p>
          <p v-if="userHasPermission">Clicking the button beside anyone will add a Loot entry, and update their BIS List accordingly (where possible).</p>
          <template v-if="displayItem.indexOf('augment') !== -1">
            <NeedTomeItemBox :user-has-permission="userHasPermission" :items-received="getNeedReceived(entry)" :entry="entry" :requesting="requesting" v-for="entry in loot.gear[displayItem].need" :key="entry.character_id" v-on:save="() => { giveNeedTomeLoot(entry) }" />
          </template>
          <template v-else-if="displayItem !== 'na'">
            <NeedRaidItemBox :user-has-permission="userHasPermission" :items-received="getNeedReceived(entry)" :entry="entry" :requesting="requesting" v-for="entry in loot.gear[displayItem].need" :key="entry.character_id" v-on:save="() => { giveNeedRaidLoot(entry) }" />
          </template>
        </div>
      </div>
    </div>

    <!-- Greed -->
    <div class="column is-half">
      <div class="card">
        <div class="card-header">
          <div class="card-header-title">
            Greed
          </div>
        </div>
        <div class="card-content">
          <p>Below are the people that need the chosen item for any other BIS they have, grouped by character.</p>
          <p v-if="userHasPermission">Clicking the button beside anyone will add a Loot entry, and update their BIS List accordingly (where possible).</p>

          <template v-if="displayItem !== 'na'">
            <GreedCharacterEntry
              v-for="entry in loot.gear[displayItem].greed"
              :key="`greed-${entry.member_id}`"

              :user-has-permission="userHasPermission"
              :items-received="getGreedReceived(entry)"
              :entry="entry"
              :requesting="requesting"
              :raid="displayItem.indexOf('augment') === -1"

              v-on:save-tome="() => { giveGreedTomeLoot(entry) }"
              v-on:save-raid="(list) => { giveGreedRaidLoot(entry, list) }"
            />
          </template>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import dayjs from 'dayjs'
import { Component, Prop, Vue } from 'vue-property-decorator'
import GreedCharacterEntry from '@/components/loot/greed_character_entry.vue'
import History from '@/components/loot/history.vue'
import ItemDropdown from '@/components/item_dropdown.vue'
import NeedRaidItemBox from '@/components/loot/need_raid_item_box.vue'
import NeedTomeItemBox from '@/components/loot/need_tome_item_box.vue'
import {
  GreedGear,
  GreedItem,
  NeedGear,
  Loot,
  LootData,
  LootPacket,
  LootWithBISPacket,
  TomeGreedGear,
  TomeNeedGear,
} from '@/interfaces/loot'
import { LootCreateErrors, LootBISCreateErrors } from '@/interfaces/responses'

@Component({
  components: {
    GreedCharacterEntry,
    History,
    ItemDropdown,
    NeedRaidItemBox,
    NeedTomeItemBox,
  },
})
export default class PerItemLootManager extends Vue {
  errors: LootBISCreateErrors = {}

  displayItem = 'na'

  @Prop()
  loot!: LootData

  @Prop()
  requesting!: boolean

  @Prop()
  sendLoot!: (data: LootPacket) => Promise<LootCreateErrors | null>

  @Prop()
  sendLootWithBis!: (data: LootWithBISPacket) => Promise<LootBISCreateErrors | null>

  @Prop()
  userHasPermission!: boolean

  getGreedReceived(entry: GreedGear): number {
    // Given an entry, search the history and find how many times that Character has received greed loot so far this tier
    return this.loot.history.reduce((sum: number, loot: Loot) => sum + (loot.member === entry.character_name && loot.greed ? 1 : 0), 0)
  }

  getNeedReceived(entry: NeedGear): number {
    // Given an entry, search the history and find how many times that Character has received need loot so far this tier
    return this.loot.history.reduce((sum: number, loot: Loot) => sum + (loot.member === entry.character_name && !loot.greed ? 1 : 0), 0)
  }

  // Functions to handle interacting with the API for handling loot handouts
  giveGreedRaidLoot(entry: GreedGear, list: GreedItem): void {
    const data = {
      greed: true,
      greed_bis_id: list.bis_list_id,
      member_id: entry.member_id,
      item: this.displayItem,
    }
    this.trackBisLoot(data)
  }

  // Tome loot sends information using the non bis api -> tracks history, no BIS updates
  giveGreedTomeLoot(entry: TomeGreedGear): void {
    const data = {
      greed: true,
      obtained: dayjs().format('YYYY-MM-DD'),
      member_id: entry.member_id,
      item: this.displayItem,
    }
    this.sendLoot(data)
  }

  giveNeedRaidLoot(entry: NeedGear): void {
    const data = {
      greed: false,
      greed_bis_id: null,
      member_id: entry.member_id,
      item: this.displayItem,
    }
    this.trackBisLoot(data)
  }

  giveNeedTomeLoot(entry: TomeNeedGear): void {
    const data = {
      greed: false,
      obtained: dayjs().format('YYYY-MM-DD'),
      member_id: entry.member_id,
      item: this.displayItem,
    }
    this.sendLoot(data)
  }

  // Helper function that sits inbetween the giveRaidLoot and sendLootWithBis functions
  async trackBisLoot(data: LootWithBISPacket): Promise<void> {
    this.errors = {}
    const response = await this.sendLootWithBis(data)
    if (response !== null) {
      this.errors = response
    }
  }
}
</script>

<style lang="scss">
.card-content .box:first-of-type {
  margin-top: 0.5rem;
}

.list-item:not(:last-child) {
  margin-bottom: 1.5rem;
}

.list-item, .list-data, .left, .right {
  display: flex;
  align-items: center;

  & .tags, .tag {
    margin:0;
  }
}

.list-item .tags {
  margin-right: 0.5rem;
}

.list-data, .left {
  flex-grow: 1;
}

.list-actions {
  margin-left: 1.25rem;
}
</style>
