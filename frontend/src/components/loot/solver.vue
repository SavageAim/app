<template>
  <div class="card">
    <a class="card-header" @click="toggleShown" v-if="loaded">
      <div class="card-header-title">
        Loot Solver
      </div>
      <div class="card-header-icon">
        <i class="material-icons" v-if="!isShown">expand_more</i>
        <i class="material-icons" v-else>expand_less</i>
      </div>
    </a>
    <div class="card-header solver-loading" v-else>
      <div class="card-header-title">
        Loot Solver
      </div>
      <div class="card-header-icon">
        <span class="solver-loading-spinner"></span>
      </div>
    </div>
    <div class="card-content" :class="{'is-hidden': !isShown}">
      <ul class="is-hidden-desktop mobile-solver-data" v-if="loaded">
        <li>
          <b>Fight: </b> {{ tier.fights[0] }}<br />
          <b>Kills Remaining: </b> {{ data.first_floor.length }}<br />
          <b>Token Purchase: </b> <span v-if="data.first_floor[0].token">Yes!</span><span v-else>No!</span>
          <button class="button is-primary is-fullwidth" v-if="shouldShowAssignButton" @click="autoAssignFirstFloor">
            <span class="icon-text">
              <span class="icon"><i class="material-icons">upload</i></span>
              <span>Auto-Assign Loot</span>
            </span>
          </button>
          <button class="button is-dark is-link is-fullwidth">
            <span class="icon-text">
              <span class="icon"><i class="material-icons">insights</i></span>
              <span>See Distribution</span>
            </span>
          </button>
        </li>
        <li>
          <b>Fight: </b> {{ tier.fights[1] }}<br />
          <b>Kills Remaining: </b> {{ data.second_floor.length }}<br />
          <b>Token Purchase: </b> <span v-if="data.second_floor[0].token">Yes!</span><span v-else>No!</span>
          <button class="button is-primary is-fullwidth" v-if="shouldShowAssignButton" @click="autoAssignSecondFloor">
            <span class="icon-text">
              <span class="icon"><i class="material-icons">upload</i></span>
              <span>Auto-Assign Loot</span>
            </span>
          </button>
          <button class="button is-dark is-link is-fullwidth">
            <span class="icon-text">
              <span class="icon"><i class="material-icons">insights</i></span>
              <span>See Distribution</span>
            </span>
          </button>
        </li>
        <li>
          <b>Fight: </b> {{ tier.fights[2] }}<br />
          <b>Kills Remaining: </b> {{ data.third_floor.length }}<br />
          <b>Token Purchase: </b> <span v-if="data.third_floor[0].token">Yes!</span><span v-else>No!</span>
          <button class="button is-primary is-fullwidth" v-if="shouldShowAssignButton" @click="autoAssignThirdFloor">
            <span class="icon-text">
              <span class="icon"><i class="material-icons">upload</i></span>
              <span>Auto-Assign Loot</span>
            </span>
          </button>
          <button class="button is-dark is-link is-fullwidth">
            <span class="icon-text">
              <span class="icon"><i class="material-icons">insights</i></span>
              <span>See Distribution</span>
            </span>
          </button>
        </li>
        <li>
          <b>Fight: </b> {{ tier.fights[3] }}<br />
          <b>Weapons Remaining: </b> {{ data.fourth_floor.weapons }}<br />
          <b>Mounts Remaining: </b> {{ data.fourth_floor.weapons }}
        </li>
      </ul>

      <!-- Desktop View -->
      <table class="table is-striped is-bordered is-fullwidth is-hidden-touch has-text-centered solver-table" v-if="loaded">
        <thead>
          <tr>
            <th>Fight</th>
            <th>Kills Remaining</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <!-- First Floor -->
          <tr>
            <th rowspan="2">{{ tier.fights[0] }}</th>
            <td>{{ data.first_floor.length }}</td>
            <td>
              <div class="field has-addons">
                <div class="control is-expanded" v-if="shouldShowAssignButton">
                  <button class="button is-primary is-fullwidth" @click="autoAssignFirstFloor">
                    <span class="icon-text">
                      <span class="icon"><i class="material-icons">upload</i></span>
                      <span>Auto-Assign Loot</span>
                    </span>
                  </button>
                </div>
                <div class="control is-expanded" v-if="data.first_floor.length > 0" @click="showFirstFloorDistribution">
                  <button class="button is-dark is-link is-fullwidth">
                    <span class="icon-text">
                      <span class="icon"><i class="material-icons">insights</i></span>
                      <span>See Distribution</span>
                    </span>
                  </button>
                </div>
              </div>
            </td>
          </tr>
          <tr>
            <td colspan="2">
              <span v-if="data.first_floor[0].token">Token Purchase This Kill!</span>
              <span v-else>No Token Purchase This Kill!</span>
            </td>
          </tr>
          <!-- Second Floor -->
          <tr>
            <th rowspan="2">{{ tier.fights[1] }}</th>
            <td>{{ data.second_floor.length }}</td>
            <td>
              <div class="field has-addons">
                <div class="control is-expanded" v-if="shouldShowAssignButton">
                  <button class="button is-primary is-fullwidth" @click="autoAssignSecondFloor">
                    <span class="icon-text">
                      <span class="icon"><i class="material-icons">upload</i></span>
                      <span>Auto-Assign Loot</span>
                    </span>
                  </button>
                </div>
                <div class="control is-expanded" v-if="data.second_floor.length > 0" @click="showSecondFloorDistribution">
                  <button class="button is-dark is-link is-fullwidth">
                    <span class="icon-text">
                      <span class="icon"><i class="material-icons">insights</i></span>
                      <span>See Distribution</span>
                    </span>
                  </button>
                </div>
              </div>
            </td>
          </tr>
          <tr>
            <td colspan="2">
              <span v-if="data.second_floor[0].token">Token Purchase This Kill!</span>
              <span v-else>No Token Purchase This Kill!</span>
            </td>
          </tr>

          <!-- Third Floor -->
          <tr>
            <th rowspan="2">{{ tier.fights[2] }}</th>
            <td>{{ data.third_floor.length }}</td>
            <td>
              <div class="field has-addons">
                <div class="control is-expanded" v-if="shouldShowAssignButton">
                  <button class="button is-primary is-fullwidth" @click="autoAssignThirdFloor">
                    <span class="icon-text">
                      <span class="icon"><i class="material-icons">upload</i></span>
                      <span>Auto-Assign Loot</span>
                    </span>
                  </button>
                </div>
                <div class="control is-expanded" v-if="data.third_floor.length > 0" @click="showThirdFloorDistribution">
                  <button class="button is-dark is-link is-fullwidth">
                    <span class="icon-text">
                      <span class="icon"><i class="material-icons">insights</i></span>
                      <span>See Distribution</span>
                    </span>
                  </button>
                </div>
              </div>
            </td>
          </tr>
          <tr>
            <td colspan="2">
              <span v-if="data.third_floor[0].token">Token Purchase This Kill!</span>
              <span v-else>No Token Purchase This Kill!</span>
            </td>
          </tr>

          <!-- Fourth Floor -->
          <tr>
            <th rowspan="2">{{ tier.fights[3] }}</th>
            <td rowspan="2">
              <div>Weapons Needed: {{ data.fourth_floor.weapons }}</div>
              <div>Mounts Needed: {{ data.fourth_floor.mounts }}</div>
            </td>
          </tr>
          <tr>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script lang="ts">
import * as Sentry from '@sentry/vue'
import { Component, Prop } from 'vue-property-decorator'
import { LootSolverData } from '@/interfaces/loot_solver'
import SavageAimMixin from '@/mixins/savage_aim_mixin'
import Tier from '@/interfaces/tier'
import LootSolverDistributionTable from '@/components/modals/loot_solver_distribution.vue'

@Component
export default class LootSolver extends SavageAimMixin {
  loaded = false

  data!: LootSolverData

  isShown = false

  @Prop()
  lootManagerType!: string

  @Prop()
  teamMemberNames!: { [id: number]: string }

  @Prop()
  tier!: Tier

  @Prop()
  url!: string

  @Prop()
  userHasPermission!: boolean

  get shouldShowAssignButton(): boolean {
    return this.userHasPermission && this.lootManagerType === 'fight'
  }

  autoAssignFirstFloor(): void {
    this.$emit('auto-assign-first-floor', this.data.first_floor[0])
  }

  autoAssignSecondFloor(): void {
    this.$emit('auto-assign-second-floor', this.data.second_floor[0])
  }

  autoAssignThirdFloor(): void {
    this.$emit('auto-assign-third-floor', this.data.third_floor[0])
  }

  async fetchData(reload: boolean): Promise<void> {
    // Load the solver data from the API
    this.loaded = false
    try {
      // Pick a URL at random, 50% odds each time
      const response = await fetch(this.url)

      if (response.ok) {
        // Parse the JSON and save it in instance variables
        this.data = (await response.json()) as LootSolverData
        console.log(this.data)
        this.loaded = true
        if (reload) this.$forceUpdate()
      }
      else {
        super.handleError(response.status)
      }
    }
    catch (e) {
      this.$notify({ text: `Error ${e} when fetching Loot Solver Data.`, type: 'is-danger' })
      Sentry.captureException(e)
    }
  }

  mounted(): void {
    this.fetchData(false)
  }

  showFirstFloorDistribution(): void {
    this.$modal.show(LootSolverDistributionTable, { data: this.data.first_floor, fight: this.tier.fights[0], teamMemberNames: this.teamMemberNames })
  }

  showSecondFloorDistribution(): void {
    this.$modal.show(LootSolverDistributionTable, { data: this.data.second_floor, fight: this.tier.fights[1], teamMemberNames: this.teamMemberNames })
  }

  showThirdFloorDistribution(): void {
    this.$modal.show(LootSolverDistributionTable, { data: this.data.third_floor, fight: this.tier.fights[2], teamMemberNames: this.teamMemberNames })
  }

  // Hide / Show the History body
  toggleShown(): void {
    this.isShown = !this.isShown
  }
}
</script>

<style lang="scss">
.mobile-solver-data li:not(:last-child) {
  margin-bottom: 0.75rem;
  padding-bottom: 0.75rem;
  border-bottom: 2px solid #17181c;
}

.solver-loading .card-header-icon {
  cursor: default;
}

table.solver-table {
  & th, & td {
    vertical-align: middle;
  }
}
</style>
