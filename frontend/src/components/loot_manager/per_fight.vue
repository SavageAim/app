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

      <template v-if="fight != 'na' && userHasPermission">
        <button class="button is-success is-fullwidth" @click="save" v-if="!(requesting || requestingI)">Save Loot Assigments</button>
        <button class="button is-success is-fullwidth is-loading" v-else>Save Loot Assigments</button>
      </template>
    </div>

    <div class="column" v-for="item in fightItems()" :key="item">
      <div class="card">
        <div class="card-header">
          <div class="card-header-title">
            {{ item }}
          </div>
        </div>
        <div class="card-content">
          <a class="box" @click="() => { selectTeamMember(item) }" v-if="!chosenMembers[item]">
            Select a Team Member
          </a>
          <a class="box list-data" @click="() => { selectTeamMember(item) }" v-else>
            <span class="badge" :class="chosenMembers[item].greed ? 'is-info' : 'is-primary'">{{ chosenMembers[item].items_received }}</span>
            <div class="left">
              {{ chosenMembers[item].member_name }}
            </div>
            <div class="right">
              <span class="icon" v-if="chosenMembers[item].job_id !== null">
                <img :src="`/job_icons/${chosenMembers[item].job_id}.png`" :alt="`${chosenMembers[item].job_id} job icon`" width="24" height="24" />
              </span>
            </div>
          </a>
        </div>
        <footer class="card-footer" v-if="chosenMembers[item]">
          <a class="card-footer-item has-text-danger" @click="() => { clear(item) }">Clear</a>
        </footer>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import dayjs from 'dayjs'
import {
  Component,
  Prop,
  Vue,
  Watch,
} from 'vue-property-decorator'
import GreedCharacterEntry from '@/components/loot/greed_character_entry.vue'
import History from '@/components/loot/history.vue'
import ItemDropdown from '@/components/item_dropdown.vue'
import NeedRaidItemBox from '@/components/loot/need_raid_item_box.vue'
import NeedTomeItemBox from '@/components/loot/need_tome_item_box.vue'
import PerFightMemberSelect from '@/components/modals/per_fight_member_select.vue'
import {
  LootData,
  LootGear,
  LootPacket,
  LootWithBISPacket,
  PerFightChosenMember,
} from '@/interfaces/loot'
import { LootCreateErrors, LootBISCreateErrors } from '@/interfaces/responses'
import Tier from '@/interfaces/tier'
import SavageAimMixin from '@/mixins/savage_aim_mixin'

@Component({
  components: {
    GreedCharacterEntry,
    History,
    ItemDropdown,
    NeedRaidItemBox,
    NeedTomeItemBox,
  },
})
export default class PerFightLootManager extends SavageAimMixin {
  chosenMembers: { [item: string]: PerFightChosenMember } = {}

  errors: LootBISCreateErrors = {}

  @Prop()
  fetchData!: (refresh: boolean) => void

  fight = 'na'

  @Prop()
  loot!: LootData

  @Prop()
  requesting!: boolean

  // Internal requesting flag so the button doesn't stop and start spinning
  requestingI = false

  @Prop()
  tier!: Tier

  @Prop()
  url!: string

  @Prop()
  userHasPermission!: boolean

  chooseMember(data: PerFightChosenMember, item: string): void {
    this.chosenMembers[item] = data
    this.$forceUpdate()
  }

  clear(item: string) {
    delete this.chosenMembers[item]
    this.$forceUpdate()
  }

  @Watch('fight')
  emptyChosenMembers(): void {
    // When you change the fight, reset the chosen map
    this.chosenMembers = {}
  }

  get fightItemMap(): {[key: string]: string[]} {
    // Temp solution
    return {
      na: [],
      first: ['Earrings', 'Necklace', 'Bracelet', 'Ring'],
      second: ['Head', 'Hands', 'Feet', 'Tome Accessory Augment', 'Tome Weapon Token'],
      third: ['Body', 'Legs', 'Tome Armour Augment', 'Tome Weapon Augment'],
      fourth: ['Mainhand Drop', 'Mainhand Coffer', 'Mount'],
    }
  }

  fightItems(): string[] {
    return this.fightItemMap[this.fight]
  }

  async save(): Promise<void> {
    // Don't do anything if no members are chosen
    if (Object.keys(this.chosenMembers).length === 0) return

    // Set the internal requesting flag
    this.requestingI = true

    // Maintain an array of responses for error displaying
    const responses: (LootCreateErrors | LootBISCreateErrors | null)[] = []

    // Iterate through our chosen members and upload their data
    const entries = Object.entries(this.chosenMembers)
    // Have to use this loop type to properly await all responses
    /* eslint-disable no-await-in-loop */
    for (let index = 0; index < entries.length; index += 1) {
      const [item, data] = entries[index]
      let key = item.toLowerCase().replaceAll(' ', '-')
      // Special case handling for mainhand differentiations
      if (key.indexOf('mainhand') !== -1) key = 'mainhand'
      const lootPacket = {
        greed: data.greed,
        greed_bis_id: data.greed_list_id,
        obtained: dayjs().format('YYYY-MM-DD'),
        member_id: data.member_id,
        item: key,
      }

      // If the flag is greed but no greed id is given, send without update (will only happen when it's `give to a char`)
      if (lootPacket.greed && lootPacket.greed_bis_id === null) {
        responses.push(await this.sendLoot(lootPacket))
      }
      // Check if the key is one of the tome items or the mount
      else if (key === 'mount' || key.indexOf('tome') !== -1) {
        responses.push(await this.sendLoot(lootPacket))
      }
      // Anything else will get sent with a bis update request
      else {
        responses.push(await this.sendLootWithBis(lootPacket))
      }
    }
    /* eslint-enable no-await-in-loop */

    // Select a notification type to display based on how the requests went
    const tester = (value: LootCreateErrors | LootBISCreateErrors | null) => value === null
    if (responses.every(tester)) {
      // All responses were successful. Give green message, clear selected inputs, and reload the state
      this.$notify({ text: 'All Loot was recorded successfully!', type: 'is-success' })
      this.chosenMembers = {}
      this.fetchData(true)
    }
    // If we reach here, there has to be at least one non-null value
    // If there are some successful requests then display details to that effect
    else if (responses.find(tester) === null) {
      this.$notify({ text: 'Some of the requests failed. This should not normally happen and has been reported.', type: 'is-warning' })
      // TODO - Remove the successful ones from the data and display error messages for the others.
    }
    else {
      // All failed, just display error messages
      this.$notify({ text: 'All requests failed. This should not normally happen and has been reported.', type: 'is-danger' })
    }

    // Reset the state
    this.requestingI = false
  }

  selectTeamMember(item: string): void {
    let key = item.toLowerCase().replaceAll(' ', '-') as keyof LootGear
    // Special case handling for mainhand differentiations
    if (key.indexOf('mainhand') !== -1) key = 'mainhand'
    this.$modal.show(
      PerFightMemberSelect,
      {
        choose: this.chooseMember,
        greed: this.loot.gear[key].greed,
        item,
        need: this.loot.gear[key].need,
        received: this.loot.received,
      },
    )
  }

  async sendLoot(data: LootPacket): Promise<LootCreateErrors | null> {
    // Send a request to create loot entry without affecting bis lists
    const body = JSON.stringify(data)
    try {
      const response = await fetch(this.url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': this.$cookies.get('csrftoken'),
        },
        body,
      })

      if (!response.ok) {
        super.handleError(response.status)
        return await response.json() as LootCreateErrors
      }
    }
    catch (e) {
      this.$notify({ text: `Unexpected error ${e} when attempting to add Loot entry.`, type: 'is-danger' })
    }
    return null
  }

  async sendLootWithBis(data: LootWithBISPacket): Promise<LootBISCreateErrors | null> {
    // Regardless of whichever type of button is pressed, send a request to create a loot entry
    const body = JSON.stringify(data)
    try {
      const response = await fetch(`${this.url}bis/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': this.$cookies.get('csrftoken'),
        },
        body,
      })

      if (!response.ok) {
        super.handleError(response.status)
        return (await response.json() as LootBISCreateErrors)
      }
    }
    catch (e) {
      this.$notify({ text: `Unexpected error ${e} when attempting to add Loot entry.`, type: 'is-danger' })
    }
    return null
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

.box.list-data {
  position: relative;
}
</style>
