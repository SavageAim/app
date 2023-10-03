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
      />

      <PerFightLootManager
        :fetch-data="fetchData"
        :loot="loot"
        :requesting="requesting"
        :tier="team.tier"
        :url="url"
        :user-has-permission="userHasLootManagerPermission"
        v-if="version === 'fight'"
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
      />
    </template>
  </div>
</template>

<script lang="ts">
import { Component } from 'vue-property-decorator'
import History from '@/components/loot/history.vue'
import PerFightLootManager from '@/components/loot_manager/per_fight.vue'
import PerItemLootManager from '@/components/loot_manager/per_item.vue'
import TeamNav from '@/components/team/nav.vue'
import {
  LootData,
  LootPacket,
  LootResponse,
  LootWithBISPacket,
} from '@/interfaces/loot'
import { LootCreateErrors, LootBISCreateErrors } from '@/interfaces/responses'
import Team from '@/interfaces/team'
import TeamViewMixin from '@/mixins/team_view_mixin'

@Component({
  components: {
    History,
    PerFightLootManager,
    PerItemLootManager,
    TeamNav,
  },
})
export default class TeamLoot extends TeamViewMixin {
  loaded = false

  loot!: LootData

  requesting = false

  team!: Team

  get url(): string {
    return `/backend/api/team/${this.teamId}/loot/`
  }

  get version(): string {
    return this.$store.state.user.loot_manager_version
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
    }
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
      }
      else {
        super.handleError(response.status)
        this.$notify({ text: `Unexpectedly received an error when giving out an item. Error messages have been added to the page. This is probably something wrong with the site itself.`, type: 'is-danger' })
        return (await response.json() as LootBISCreateErrors)
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
