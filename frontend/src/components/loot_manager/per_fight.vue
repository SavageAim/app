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
                <option value="first">{{ tier.fights[0] }}</option>
                <option value="second">{{ tier.fights[1] }}</option>
                <option value="third">{{ tier.fights[2] }}</option>
                <option value="fourth">{{ tier.fights[3] }}</option>
              </select>
            </div>
          </div>
          <p class="has-text-primary" v-if="fight != 'na' && userHasPermission">Click on the dark boxes to pick a Team Member to get each item, then click the Save button to update everyone's loot at once.</p>

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
      <button class="button is-success is-fullwidth" v-if="fight != 'na' && userHasPermission">Save Loot Assigments</button>
    </div>

    <div class="column" v-for="item in fightItems()" :key="item">
      <div class="card">
        <div class="card-header">
          <div class="card-header-title">
            {{ item }}
          </div>
        </div>
        <div class="card-content">
          <a class="box" @click="() => { selectTeamMember(item) }">
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
import PerFightMemberSelect from '@/components/modals/per_fight_member_select.vue'
import {
  GreedGear,
  GreedItem,
  NeedGear,
  LootData,
  LootGear,
  LootPacket,
  LootWithBISPacket,
  TomeGreedGear,
  TomeNeedGear,
} from '@/interfaces/loot'
import { LootCreateErrors, LootBISCreateErrors } from '@/interfaces/responses'
import Tier from '@/interfaces/tier'

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
  tier!: Tier

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

  selectTeamMember(item: string): void {
    const key = item.toLowerCase().replaceAll(' ', '-') as keyof LootGear
    this.$modal.show(
      PerFightMemberSelect,
      {
        greed: this.loot.gear[key].greed,
        item,
        need: this.loot.gear[key].need,
        received: this.loot.received,
      },
    )
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
