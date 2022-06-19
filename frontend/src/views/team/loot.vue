<template>
  <div>
    <div v-if="!loaded">
      <button class="button is-static is-loading is-fullwidth">Loading</button>
    </div>

    <template v-else>
      <div class="level">
        <div class="level-left">
          <div class="level-item">
            <h2 class="title is-spaced">{{ team.name }}</h2>
            <div class="icon-text subtitle is-hidden-touch">
              <span class="icon"><i class="material-icons">room</i></span>
              <span>{{ team.tier.name }}</span>
            </div>
          </div>
        </div>

        <div class="level-right">
          <div class="level-item">
            <TeamNav :editable="editable" />
          </div>
        </div>
      </div>

      <div class="columns is-dekstop is-multiline">
        <div class="column is-full">
          <div class="card">
            <div class="card-header">
              <div class="card-header-title">
                What Item Dropped
              </div>
            </div>
            <div class="card-content">
              <ItemDropdown v-model="displayItem" />

              <!-- Display generic errors here -->
              <div class="box has-background-danger" v-if="bisLootErrors.greed !== undefined">
                <b>Greed: </b> {{ bisLootErrors.greed[0] }}
              </div>
              <div class="box has-background-danger" v-if="bisLootErrors.greed_bis_id !== undefined">
                <b>Greed BIS ID:</b> {{ bisLootErrors.greed_bis_id[0] }}
              </div>
              <div class="box has-background-danger" v-if="bisLootErrors.item !== undefined">
                <b>Item: </b> {{ bisLootErrors.item[0] }}
              </div>
              <div class="box has-background-danger" v-if="bisLootErrors.member_id !== undefined">
                <b>Member ID:</b> {{ bisLootErrors.member_id[0] }}
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
              <p v-if="editable">Clicking the button beside anyone will add a Loot entry, and update their BIS List accordingly (where possible).</p>
              <template v-if="displayItem.indexOf('augment') !== -1">
                <NeedTomeItemBox :editable="editable" :items-received="getNeedReceived(entry)" :entry="entry" :requesting="requesting" v-for="entry in loot.gear[displayItem].need" :key="entry.character_id" v-on:save="() => { giveNeedTomeLoot(entry) }" />
              </template>
              <template v-else-if="displayItem !== 'na'">
                <NeedRaidItemBox :editable="editable" :items-received="getNeedReceived(entry)" :entry="entry" :requesting="requesting" v-for="entry in loot.gear[displayItem].need" :key="entry.character_id" v-on:save="() => { giveNeedRaidLoot(entry) }" />
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
              <p v-if="editable">Clicking the button beside anyone will add a Loot entry, and update their BIS List accordingly (where possible).</p>

              <template v-if="displayItem !== 'na'">
                <GreedCharacterEntry
                  v-for="entry in loot.gear[displayItem].greed"
                  :key="`greed-${entry.member_id}`"

                  :editable="editable"
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

        <History
          :fetch-data="fetchData"
          :loot="loot"
          :sendLoot="sendLoot"
          :requesting="requesting"
          :team="team"
          :url="url"
        />
      </div>
    </template>
  </div>
</template>

<script lang="ts">
import dayjs from 'dayjs'
import { Component } from 'vue-property-decorator'
import GreedCharacterEntry from '@/components/loot/greed_character_entry.vue'
import History from '@/components/loot/history.vue'
import ItemDropdown from '@/components/item_dropdown.vue'
import NeedRaidItemBox from '@/components/loot/need_raid_item_box.vue'
import NeedTomeItemBox from '@/components/loot/need_tome_item_box.vue'
import TeamNav from '@/components/team/nav.vue'
import {
  GreedGear,
  GreedItem,
  NeedGear,
  Loot,
  LootData,
  LootPacket,
  LootResponse,
  LootWithBISPacket,
  TomeGreedGear,
  TomeNeedGear,
} from '@/interfaces/loot'
import { LootCreateErrors, LootBISCreateErrors } from '@/interfaces/responses'
import Team from '@/interfaces/team'
import TeamMember from '@/interfaces/team_member'
import SavageAimMixin from '@/mixins/savage_aim_mixin'

@Component({
  components: {
    GreedCharacterEntry,
    History,
    ItemDropdown,
    NeedRaidItemBox,
    NeedTomeItemBox,
    TeamNav,
  },
})
export default class TeamLoot extends SavageAimMixin {
  bisLootErrors: LootBISCreateErrors = {}

  displayItem = 'na'

  loaded = false

  loot!: LootData

  requesting = false

  team!: Team

  // Flag stating whether the currently logged user can edit the Team
  get editable(): boolean {
    return this.team.members.find((teamMember: TeamMember) => teamMember.character.user_id === this.$store.state.user.id)?.permissions.loot_manager ?? false
  }

  get url(): string {
    return `/backend/api/team/${this.$route.params.id}/loot/`
  }

  async created(): Promise<void> {
    await this.fetchData(false)
    document.title = `Loot Tracker - ${this.team.name} - Savage Aim`
  }

  async fetchData(reload: boolean): Promise<void> {
    // Load the loot data from the API
    try {
      const response = await fetch(this.url)
      if (response.ok) {
        // Parse the JSON and save it in instance variables
        const content = (await response.json()) as LootResponse
        this.team = content.team
        this.loot = content.loot
        this.loaded = true
        if (reload) this.$forceUpdate()
      }
      else {
        super.handleError(response.status)
      }
    }
    catch (e) {
      this.$notify({ text: `Error ${e} when fetching Team Loot Data.`, type: 'is-danger' })
    }
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
      item: this.displayItem,
    }
    this.sendLootWithBis(data)
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
    this.sendLootWithBis(data)
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

  // Reload called via websockets
  async load(): Promise<void> {
    this.fetchData(true)
  }

  async sendLoot(data: LootPacket): Promise<LootCreateErrors | null> {
    // Send a request to create loot entry without affecting bis lists
    if (this.requesting) return null
    this.requesting = true
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

      if (response.ok) {
        await this.fetchData(true)
        this.$notify({ text: 'Loot updated!', type: 'is-success' })
      }
      else {
        super.handleError(response.status)
        return await response.json() as LootCreateErrors
      }
    }
    catch (e) {
      this.$notify({ text: `Error ${e} when attempting to add Loot entry.`, type: 'is-danger' })
    }
    finally {
      this.requesting = false
    }
    return null
  }

  async sendLootWithBis(data: LootWithBISPacket): Promise<void> {
    // Regardless of whichever type of button is pressed, send a request to create a loot entry
    if (this.requesting) return
    this.requesting = true
    this.bisLootErrors = {}
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

      if (response.ok) {
        await this.fetchData(true)
        this.$notify({ text: 'Loot updated!', type: 'is-success' })
      }
      else {
        super.handleError(response.status)
        this.bisLootErrors = (await response.json() as LootBISCreateErrors)
        this.$notify({ text: `Unexpectedly received an error when giving out an item. Error messages have been added to the page. This is probably something wrong with the site itself.`, type: 'is-danger' })
      }
    }
    catch (e) {
      this.$notify({ text: `Error ${e} when attempting to add Loot entry.`, type: 'is-danger' })
    }
    finally {
      this.requesting = false
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
