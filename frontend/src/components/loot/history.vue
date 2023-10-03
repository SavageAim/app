<template>
  <div>
    <div class="card">
      <a class="card-header" @click="toggleHistory">
        <div class="card-header-title">
          Tier Loot History
        </div>
        <div class="card-header-icon">
          <span class="icon"><i class="material-icons" ref="historyIcon">expand_more</i></span>
        </div>
      </a>
      <div class="card-content is-hidden" ref="history">
        <ul class="is-hidden-desktop mobile-history">
          <!-- Edit row -->
          <li v-if="userHasPermission">
            <h3 class="subtitle">Add Entry</h3>
            <div class="field is-horizontal">
              <div class="field-label is-normal">
                <label class="label">Obtained</label>
              </div>
              <div class="field-body">
                <div class="field">
                  <div class="control">
                    <input class="input" type="date" v-model="createData.obtained" />
                    <p class="help is-danger" v-if="errors.obtained !== undefined">{{ errors.obtained[0] }}</p>
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
                        <option v-for="member in team.members" :key="member.id" :value="member.id">{{ member.name }}</option>
                      </select>
                    </div>
                    <p class="help is-danger" v-if="errors.member_id !== undefined">{{ errors.member_id[0] }}</p>
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
                  <ItemDropdown v-model="createData.item" :error="errors.item" />
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
                    <p class="help is-danger" v-if="errors.greed !== undefined">{{ errors.greed[0] }}</p>
                  </div>
                </div>
              </div>
            </div>
          </li>

          <li v-for="history in loot.history" :key="`mobile-history-${history.id}`">
            <b>Item: </b> {{ history.item }}<br />
            <b>Obtained By: </b> {{ history.member }}<br />
            <button v-if="userHasPermission" class="button is-danger is-pulled-right" @click="() => { deleteEntries([history]) }">
              <i class="material-icons">delete</i>
            </button>
            <b>On: </b> {{ history.obtained }}<br />
            <b>Via: </b>
            <span class="has-text-info" v-if="history.greed">Greed</span>
            <span class="has-text-primary" v-else>Need</span>
          </li>
        </ul>

        <!-- Desktop View -->
        <table class="table is-striped is-bordered is-fullwidth is-hidden-touch">
          <thead>
            <tr>
              <th>Date</th>
              <th>Obtained By</th>
              <th>Item</th>
              <th>Need / Greed</th>
              <th v-if="userHasPermission" class="delete-cell has-text-centered">Delete</th>
            </tr>
          </thead>
          <tbody>
            <!-- Edit Row -->
            <tr v-if="userHasPermission">
              <td>
                <div class="control">
                  <input class="input" type="date" v-model="createData.obtained" />
                  <p class="help is-danger" v-if="errors.obtained !== undefined">{{ errors.obtained[0] }}</p>
                </div>
              </td>
              <td>
                <div class="control">
                  <div class="select is-fullwidth">
                    <select v-model="createData.member">
                      <option value="-1">Select Team Member</option>
                      <option v-for="member in team.members" :key="member.id" :value="member.id">{{ member.name }}</option>
                    </select>
                  </div>
                  <p class="help is-danger" v-if="errors.member_id !== undefined">{{ errors.member_id[0] }}</p>
                </div>
              </td>
              <td>
                <ItemDropdown v-model="createData.item" :error="errors.item" />
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
                  <p class="help is-danger" v-if="errors.greed !== undefined">{{ errors.greed[0] }}</p>
                </div>
              </td>
              <td>
              </td>
            </tr>

            <!-- Data -->
            <tr v-for="history in loot.history" :key="`history-${history.id}`">
              <td><p>{{ history.obtained }}</p></td>
              <td><p>{{ history.member }}</p></td>
              <td><p>{{ history.item }}</p></td>
              <td>
                <p class="has-text-info" v-if="history.greed">Greed</p>
                <p class="has-text-primary" v-else>Need</p>
              </td>
              <td v-if="userHasPermission" class="delete-cell has-text-centered">
                <input type="checkbox" ref="lootDeleteCheckbox" :data-id="history.id" />
              </td>
            </tr>

            <!-- Delete Button -->
            <tr v-if="userHasPermission">
              <td></td>
              <td></td>
              <td></td>
              <td></td>
              <td>
                <button class="button is-danger" @click="deleteMultipleEntries">
                  <i class="material-icons">delete</i>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop } from 'vue-property-decorator'
import DeleteLoot from '@/components/modals/confirmations/delete_loot.vue'
import ItemDropdown from '@/components/item_dropdown.vue'
import {
  Loot,
  LootData,
  LootPacket,
} from '@/interfaces/loot'
import { LootCreateErrors } from '@/interfaces/responses'
import Team from '@/interfaces/team'
import SavageAimMixin from '@/mixins/savage_aim_mixin'

@Component({
  components: {
    ItemDropdown,
  },
})
export default class History extends SavageAimMixin {
  createData = {
    item: 'na',
    member: -1,
    obtained: '',
  }

  errors: LootCreateErrors = {}

  @Prop()
  fetchData!: (reload: boolean) => Promise<void>

  historyShown = false

  @Prop()
  loot!: LootData

  @Prop()
  sendLoot!: (data: LootPacket) => Promise<LootCreateErrors | null>

  @Prop()
  requesting!: boolean

  @Prop()
  team!: Team

  @Prop()
  url!: string

  @Prop()
  userHasPermission!: boolean

  deleteEntries(items: Loot[]): void {
    // Prompt deletion first before sending an api request (we'll use a modal instead of javascript alerts)
    this.$modal.show(DeleteLoot, { team: this.team, items }, { }, { closed: () => { this.fetchData(true) } })
  }

  deleteMultipleEntries(): void {
    const checkboxes = this.$refs.lootDeleteCheckbox as HTMLInputElement[]
    const ids = checkboxes.filter((check: HTMLInputElement) => check.checked).map((check: HTMLInputElement) => parseInt(check.dataset.id!, 10)) as number[]
    const items = this.loot.history.filter((entry: Loot) => ids.includes(entry.id))
    this.deleteEntries(items)
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

  async trackExtraLoot(greed: boolean): Promise<void> {
    this.errors = {}
    if (this.createData.obtained === '') {
      this.errors.obtained = ['Please enter a date.']
      return
    }
    const data = {
      member_id: this.createData.member,
      obtained: this.createData.obtained,
      item: this.createData.item,
      greed,
    }
    const response = await this.sendLoot(data)
    if (response === null) {
      this.createData = { item: 'na', member: -1, obtained: '' }
    }
    else {
      this.errors = response
    }
  }
}
</script>

<style lang="scss">
.mobile-history li:not(:last-child) {
  margin-bottom: 0.75rem;
  padding-bottom: 0.75rem;
  border-bottom: 2px solid #17181c;
}

.delete-cell {
  width: 0;
}
</style>
