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
      <!-- <ul class="is-hidden-desktop mobile-solver-data" v-if="loaded">
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
      </ul> -->

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
                <div class="control is-expanded">
                  <button class="button is-primary is-fullwidth">
                    <span class="icon-text">
                      <span class="icon"><i class="material-icons">upload</i></span>
                      <span>Auto-Assign Loot</span>
                    </span>
                  </button>
                </div>
                <div class="control is-expanded">
                  <button class="button is-dark is-link is-fullwidth">
                    <span class="icon-text">
                      <span class="icon"><i class="material-icons">insights</i></span>
                      <span>See All Kills</span>
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
                <div class="control is-expanded">
                  <button class="button is-primary is-fullwidth">
                    <span class="icon-text">
                      <span class="icon"><i class="material-icons">upload</i></span>
                      <span>Auto-Assign Loot</span>
                    </span>
                  </button>
                </div>
                <div class="control is-expanded">
                  <button class="button is-dark is-link is-fullwidth">
                    <span class="icon-text">
                      <span class="icon"><i class="material-icons">insights</i></span>
                      <span>See All Kills</span>
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
                <div class="control is-expanded">
                  <button class="button is-primary is-fullwidth">
                    <span class="icon-text">
                      <span class="icon"><i class="material-icons">upload</i></span>
                      <span>Auto-Assign Loot</span>
                    </span>
                  </button>
                </div>
                <div class="control is-expanded">
                  <button class="button is-dark is-link is-fullwidth">
                    <span class="icon-text">
                      <span class="icon"><i class="material-icons">insights</i></span>
                      <span>See All Kills</span>
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

@Component
export default class LootSolver extends SavageAimMixin {
  loaded = false

  data!: LootSolverData

  isShown = false

  @Prop()
  lootManagerType!: string

  @Prop()
  tier!: Tier

  @Prop()
  url!: string

  @Prop()
  userHasPermission!: boolean

  get isPerFightManager(): boolean {
    return this.lootManagerType === 'fight'
  }

  async fetchData(reload: boolean): Promise<void> {
    // Load the solver data from the API
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
