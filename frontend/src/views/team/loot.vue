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
            <TeamNav :is-lead="userIsTeamLead" :team-id="teamId" />
          </div>
        </div>
      </div>

      <!-- Select the Loot Manager Version -->
      <PerItemLootManager
        :loot="loot"
        :requesting="requesting"
        :send-loot="sendLoot"
        :send-loot-with-bis="sendLootWithBis"
        :user-has-permission="userHasLootManagerPermission"
        v-if="version === 'item'"
        ref="perItemLootManager"
      />

      <PerFightLootManager
        :fetch-data="fetchData"
        :loot="loot"
        :requesting="requesting"
        :tier="team.tier"
        :url="url"
        :user-has-permission="userHasLootManagerPermission"
        v-if="version === 'fight'"
        v-on:reload-solver="reloadSolver"
        ref="perFightLootManager"
      />

      <!-- Solver -->
      <LootSolver
        :loot-manager-type="version"
        :team-member-names="teamMemberNames"
        :tier="team.tier"
        :url="solverUrl"
        :user-has-permission="userHasLootManagerPermission"
        v-on:auto-assign-first-floor="assignFirstFloor"
        v-on:auto-assign-second-floor="assignSecondFloor"
        v-on:auto-assign-third-floor="assignThirdFloor"
        ref="lootSolver"
      />

      <!-- Render the Tier History -->
      <History
        :fetch-data="fetchData"
        :loot="loot"
        :send-loot="sendLoot"
        :requesting="requesting"
        :team="team"
        :url="url"
        :user-has-permission="userHasLootManagerPermission"
        v-on:reload-solver="reloadSolver"
      />
    </template>
  </div>
</template>

<script lang="ts">
import * as Sentry from '@sentry/vue'
import { Component } from 'vue-property-decorator'
import History from '@/components/loot/history.vue'
import LootSolver from '@/components/loot/solver.vue'
import PerFightLootManager from '@/components/loot_manager/per_fight.vue'
import PerItemLootManager from '@/components/loot_manager/per_item.vue'
import TeamNav from '@/components/team/nav.vue'
import {
  LootData,
  LootPacket,
  LootResponse,
  LootWithBISPacket,
  PerFightChosenMember,
} from '@/interfaces/loot'
import { LootCreateErrors, LootBISCreateErrors } from '@/interfaces/responses'
import Team from '@/interfaces/team'
import TeamMember from '@/interfaces/team_member'
import TeamViewMixin from '@/mixins/team_view_mixin'
import { FirstFloor, SecondFloor, ThirdFloor } from '@/interfaces/loot_solver'

@Component({
  components: {
    History,
    PerFightLootManager,
    PerItemLootManager,
    TeamNav,
    LootSolver,
  },
})
export default class TeamLoot extends TeamViewMixin {
  loaded = false

  loot!: LootData

  requesting = false

  team!: Team

  get perFightLootManager(): PerFightLootManager {
    return this.$refs.perFightLootManager as PerFightLootManager
  }

  get solver(): LootSolver {
    return this.$refs.lootSolver as LootSolver
  }

  get solverUrl(): string {
    return `${this.url}solver/`
  }

  get teamMemberNames(): { [id: number]: string } {
    const memberNames: { [id: number]: string } = {}
    this.team.members.forEach((member) => {
      memberNames[member.id] = member.name
    })
    return memberNames
  }

  get url(): string {
    return `/backend/api/team/${this.teamId}/loot/`
  }

  get version(): string {
    return this.$store.state.user.loot_manager_version
  }

  assignFirstFloor(data: FirstFloor): void {
    this.autoAssign('first', data)
  }

  assignSecondFloor(data: SecondFloor): void {
    this.autoAssign('second', data)
  }

  assignThirdFloor(data: ThirdFloor): void {
    this.autoAssign('third', data)
  }

  autoAssign(fight: string, data: FirstFloor | SecondFloor | ThirdFloor): void {
    // Turn data object into a map of item: PFCM
    const chosenMembers: { [item: string]: PerFightChosenMember } = {}
    Object.entries(data).forEach(([item, memberId]) => {
      if (item !== 'token' && memberId !== null) {
        const member = this.getTeamMember(memberId)
        const itemsObtained = this.loot.received[member.name]?.need || 0
        chosenMembers[item] = {
          greed: false,
          greed_list_id: null,
          member_id: memberId,
          member_name: member.name,
          items_received: itemsObtained,
          job_id: member.bis_list.job.id,
        }
      }
    })
    this.perFightLootManager.autoAssign(fight, chosenMembers)
  }

  async created(): Promise<void> {
    await this.fetchData(false)
    document.title = `Loot Tracker - ${this.team.name} - Savage Aim`
  }

  async fetchData(reload: boolean): Promise<void> {
    // Load the loot data from the API
    try {
      // Pick a URL at random, 50% odds each time
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
      Sentry.captureException(e)
    }
  }

  getTeamMember(memberId: number): TeamMember {
    return this.team.members.find((member: TeamMember) => member.id === memberId)!
  }

  // Reload called via websockets
  async load(): Promise<void> {
    this.fetchData(true)
  }

  // Reload the Solver
  reloadSolver(): void {
    this.solver.fetchData(true)
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
        this.reloadSolver()
      }
      else {
        super.handleError(response.status)
        return await response.json() as LootCreateErrors
      }
    }
    catch (e) {
      this.$notify({ text: `Error ${e} when attempting to add Loot entry.`, type: 'is-danger' })
      Sentry.captureException(e)
    }
    finally {
      this.requesting = false
    }
    return null
  }

  async sendLootWithBis(data: LootWithBISPacket): Promise<LootBISCreateErrors | null> {
    // Regardless of whichever type of button is pressed, send a request to create a loot entry
    if (this.requesting) return null
    this.requesting = true
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
        this.reloadSolver()
      }
      else {
        super.handleError(response.status)
        this.$notify({ text: `Unexpectedly received an error when giving out an item. Error messages have been added to the page. This is probably something wrong with the site itself.`, type: 'is-danger' })
        return (await response.json() as LootBISCreateErrors)
      }
    }
    catch (e) {
      this.$notify({ text: `Error ${e} when attempting to add Loot entry.`, type: 'is-danger' })
      Sentry.captureException(e)
    }
    finally {
      this.requesting = false
    }
    return null
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
