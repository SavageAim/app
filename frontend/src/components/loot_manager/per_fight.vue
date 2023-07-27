<template>
  <div class="columns is-desktop is-multiline">
    <div class="column is-full">
      <div class="card">
        <div class="card-header">
          <div class="card-header-title">
            Select a Fight
          </div>
        </div>
        <div class="card-content">
          <div class="field">
            <div class="select is-fullwidth">
              <select v-model="fight">
                <option value="na">Select a Fight</option>
                <option value="first">Anabaseios: The Ninth Circle</option>
                <option value="second">Anabaseios: The Tenth Circle</option>
                <option value="third">Anabaseios: The Eleventh Circle</option>
                <option value="fourth">Anabaseios: The Twelfth Circle</option>
              </select>
            </div>
          </div>

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
      <button class="button is-success is-fullwidth">Save Loot Assigments</button>
    </div>

    <div class="column" v-for="item in fightItems()" :key="item">
      <div class="card">
        <div class="card-header">
          <div class="card-header-title">
            {{ item }}
          </div>
        </div>
        <div class="card-content">
          <a class="box">
            Select a Team Member
          </a>
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
export default class PerFightLootManager extends Vue {
  errors: LootBISCreateErrors = {}

  fight = 'na'

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

  get fightItemMap(): {[key: string]: string[]} {
    // Temp solution
    return {
      na: [],
      first: ['Earrings', 'Necklace', 'Bracelet', 'Ring'],
      second: ['Head', 'Hands', 'Feet', 'Tome Accessory Augment', 'Tome Weapon Token'],
      third: ['Body', 'Legs', 'Tome Armour Augment', 'Tome Weapon Augment'],
      fourth: ['Mainhand', 'Mainhand', 'Mount'],
    }
  }

  fightItems(): string[] {
    return this.fightItemMap[this.fight]
  }

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
      item: 'TODO fix this',
      // item: this.displayItem,
    }
    this.trackBisLoot(data)
  }

  // Tome loot sends information using the non bis api -> tracks history, no BIS updates
  giveGreedTomeLoot(entry: TomeGreedGear): void {
    const data = {
      greed: true,
      obtained: dayjs().format('YYYY-MM-DD'),
      member_id: entry.member_id,
      item: 'TODO fix this',
      // item: this.displayItem,
    }
    this.sendLoot(data)
  }

  giveNeedRaidLoot(entry: NeedGear): void {
    const data = {
      greed: false,
      greed_bis_id: null,
      member_id: entry.member_id,
      item: 'TODO fix this',
      // item: this.displayItem,
    }
    this.trackBisLoot(data)
  }

  giveNeedTomeLoot(entry: TomeNeedGear): void {
    const data = {
      greed: false,
      obtained: dayjs().format('YYYY-MM-DD'),
      member_id: entry.member_id,
      item: 'TODO fix this',
      // item: this.displayItem,
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
