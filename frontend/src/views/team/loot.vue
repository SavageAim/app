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

              <template v-if="displayItem.indexOf('augment') !== -1">
                <GreedTomeItemBox :editable="editable" :items-received="getGreedReceived(entry)" :entry="entry" :requesting="requesting" v-for="entry in loot.gear[displayItem].greed" :key="entry.character_id" v-on:save="() => { giveGreedTomeLoot(entry) }" />
              </template>
              <template v-else-if="displayItem !== 'na'">
                <GreedRaidItemBox :editable="editable" :items-received="getGreedReceived(entry)" :entry="entry" :requesting="requesting" v-for="entry in loot.gear[displayItem].greed" :key="entry.character_id" v-on:save="(list) => { list === null ? giveGreedTomeLoot(entry) : giveGreedRaidLoot(entry, list) }" />
              </template>
            </div>
          </div>
        </div>

        <div class="column is-full">
          <div class="card">
            <a class="card-header" @click="toggleHistory">
              <div class="card-header-title">
                Loot History
              </div>
              <div class="card-header-icon">
                <span class="icon"><i class="material-icons" ref="historyIcon">expand_more</i></span>
              </div>
            </a>
            <div class="card-content is-hidden" ref="history">
              <ul class="is-hidden-desktop mobile-history">
                <li v-for="history in loot.history" :key="`mobile-history-${history.id}`">
                  <b>Item: </b> {{ history.item }}<br />
                  <b>Obtained By: </b> {{ history.member }}<br />
                  <b>On: </b> {{ history.obtained }}<br />
                  <b>Via: </b>
                  <span class="has-text-info" v-if="history.greed">Greed</span>
                  <span class="has-text-primary" v-else>Need</span>
                </li>
                <li v-if="editable">
                  <hr />
                  <h3 class="subtitle">Add Entry</h3>
                  <div class="field is-horizontal">
                    <div class="field-label is-normal">
                      <label class="label">Obtained</label>
                    </div>
                    <div class="field-body">
                      <div class="field">
                        <div class="control">
                          <input class="input" type="date" v-model="createData.obtained" />
                          <p class="help is-danger" v-if="createLootErrors.obtained !== undefined">{{ createLootErrors.obtained[0] }}</p>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div class="field is-horizontal">
                    <div class="field-label is-normal">
                      <label class="label">Team Member</label>
                    </div>
                    <div class="field-body">
                      <div class="field">
                        <div class="control">
                          <div class="select is-fullwidth">
                            <select v-model="createData.member">
                              <option value="-1">Select Team Member</option>
                              <option v-for="member in team.members" :key="member.id" :value="member.id">{{ member.character.name }} @ {{ member.character.world }}</option>
                            </select>
                          </div>
                          <p class="help is-danger" v-if="createLootErrors.member_id !== undefined">{{ createLootErrors.member_id[0] }}</p>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div class="field is-horizontal">
                    <div class="field-label is-normal">
                      <label class="label">Item</label>
                    </div>
                    <div class="field-body">
                      <div class="field">
                        <ItemDropdown v-model="createData.item" :displayNonGear="true" :error="createLootErrors.item" />
                      </div>
                    </div>
                  </div>
                  <div class="field is-horizontal">
                    <div class="field-body">
                      <div class="field">
                        <div class="control">
                          <div class="field has-addons" v-if="!requesting">
                            <div class="control is-expanded">
                              <button class="button is-primary is-fullwidth" @click="() => { trackExtraLoot(false) }">
                                <span>Need</span>
                              </button>
                            </div>
                            <div class="control is-expanded">
                              <button class="button is-info is-fullwidth" @click="() => { trackExtraLoot(true) }">
                                <span>Greed</span>
                              </button>
                            </div>
                          </div>
                          <div class="field has-addons" v-else>
                            <div class="control is-expanded">
                              <button class="button is-primary is-fullwidth is-loading">
                                <span>Need</span>
                              </button>
                            </div>
                            <div class="control is-expanded">
                              <button class="button is-info is-fullwidth is-loading">
                                <span>Greed</span>
                              </button>
                            </div>
                          </div>
                          <p class="help is-danger" v-if="createLootErrors.greed !== undefined">{{ createLootErrors.greed[0] }}</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </li>
              </ul>
              <table class="table is-striped is-bordered is-fullwidth is-hidden-touch">
                <thead>
                  <tr>
                    <th>Date</th>
                    <th>Obtained By</th>
                    <th>Item</th>
                    <th>Need / Greed</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="history in loot.history" :key="`history-${history.id}`">
                    <td>{{ history.obtained }}</td>
                    <td>{{ history.member }}</td>
                    <td>{{ history.item }}</td>
                    <td>
                      <p class="has-text-info" v-if="history.greed">Greed</p>
                      <p class="has-text-primary" v-else>Need</p>
                    </td>
                  </tr>
                  <tr v-if="editable">
                    <td>
                      <div class="control">
                        <input class="input" type="date" v-model="createData.obtained" />
                        <p class="help is-danger" v-if="createLootErrors.obtained !== undefined">{{ createLootErrors.obtained[0] }}</p>
                      </div>
                    </td>
                    <td>
                      <div class="control">
                        <div class="select is-fullwidth">
                          <select v-model="createData.member">
                            <option value="-1">Select Team Member</option>
                            <option v-for="member in team.members" :key="member.id" :value="member.id">{{ member.character.name }} @ {{ member.character.world }}</option>
                          </select>
                        </div>
                        <p class="help is-danger" v-if="createLootErrors.member_id !== undefined">{{ createLootErrors.member_id[0] }}</p>
                      </div>
                    </td>
                    <td>
                      <ItemDropdown v-model="createData.item" :displayNonGear="true" :error="createLootErrors.item" />
                    </td>
                    <td>
                      <div class="control">
                        <div class="field has-addons" v-if="!requesting">
                          <div class="control is-expanded">
                            <button class="button is-primary is-fullwidth" @click="() => { trackExtraLoot(false) }">
                              <span>Need</span>
                            </button>
                          </div>
                          <div class="control is-expanded">
                            <button class="button is-info is-fullwidth" @click="() => { trackExtraLoot(true) }">
                              <span>Greed</span>
                            </button>
                          </div>
                        </div>
                        <div class="field has-addons" v-else>
                          <div class="control is-expanded">
                            <button class="button is-primary is-fullwidth is-loading">
                              <span>Need</span>
                            </button>
                          </div>
                          <div class="control is-expanded">
                            <button class="button is-info is-fullwidth is-loading">
                              <span>Greed</span>
                            </button>
                          </div>
                        </div>
                        <p class="help is-danger" v-if="createLootErrors.greed !== undefined">{{ createLootErrors.greed[0] }}</p>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script lang="ts">
import dayjs from 'dayjs'
import { Component } from 'vue-property-decorator'
import GreedRaidItemBox from '@/components/loot/greed_raid_item_box.vue'
import GreedTomeItemBox from '@/components/loot/greed_tome_item_box.vue'
import ItemDropdown from '@/components/item_dropdown.vue'
import NeedRaidItemBox from '@/components/loot/need_raid_item_box.vue'
import NeedTomeItemBox from '@/components/loot/need_tome_item_box.vue'
import TeamNav from '@/components/team_nav.vue'
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
    GreedRaidItemBox,
    GreedTomeItemBox,
    ItemDropdown,
    NeedRaidItemBox,
    NeedTomeItemBox,
    TeamNav,
  },
})
export default class TeamLoot extends SavageAimMixin {
  bisLootErrors: LootBISCreateErrors = {}

  createData = {
    item: 'na',
    member: -1,
    obtained: '',
  }

  createLootErrors: LootCreateErrors = {}

  historyShown = false

  displayItem = 'na'

  loaded = false

  loot!: LootData

  requesting = false

  team!: Team

  // Flag stating whether the currently logged user can edit the Team
  get editable(): boolean {
    return this.team.members.find((teamMember: TeamMember) => teamMember.character.user_id === this.$store.state.user.id)?.lead ?? false
  }

  get url(): string {
    return `/backend/api/team/${this.$route.params.id}/loot/`
  }

  created(): void {
    this.fetchData()
  }

  async fetchData(): Promise<void> {
    // Load the loot data from the API
    try {
      const response = await fetch(this.url)
      if (response.ok) {
        // Parse the JSON and save it in instance variables
        const content = (await response.json()) as LootResponse
        this.team = content.team
        this.loot = content.loot
        this.loaded = true
        document.title = `Loot Tracker - ${this.team.name} - Savage Aim`
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

  async sendLoot(data: LootPacket): Promise<void> {
    // Send a request to create loot entry without affecting bis lists
    if (this.requesting) return
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
        await this.fetchData()
        this.$notify({ text: 'Loot updated!', type: 'is-success' })
        this.createData = { obtained: '', member: -1, item: 'na' }
        this.$forceUpdate()
      }
      else {
        super.handleError(response.status)
        this.createLootErrors = (await response.json() as LootCreateErrors)
      }
    }
    catch (e) {
      this.$notify({ text: `Error ${e} when attempting to add Loot entry.`, type: 'is-danger' })
    }
    finally {
      this.requesting = false
    }
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
        await this.fetchData()
        this.$notify({ text: 'Loot updated!', type: 'is-success' })
        this.$forceUpdate()
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

  // Hide / Show the History body
  toggleHistory(): void {
    const icon = this.$refs.historyIcon as Element
    const history = this.$refs.history as Element
    if (this.historyShown) {
      this.historyShown = false
      icon.innerHTML = 'expand_more'
    }
    else {
      this.historyShown = true
      icon.innerHTML = 'expand_less'
    }
    history.classList.toggle('is-hidden')
  }

  trackExtraLoot(greed: boolean): void {
    this.createLootErrors = {}
    if (this.createData.obtained === '') {
      this.createLootErrors.obtained = ['Please enter a date.']
      return
    }
    const data = {
      member_id: this.createData.member,
      obtained: this.createData.obtained,
      item: this.createData.item,
      greed,
    }
    this.sendLoot(data)
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

.mobile-history li:not(:last-child) {
  margin-bottom: 1.5rem;
}

.greed-box {
  position: relative;
}
</style>
