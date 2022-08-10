<template>
  <div>
    <div v-if="loading">
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
            <TeamNav :is-lead="editable" />
          </div>
        </div>
      </div>

      <div class="columns is-multiline is-desktop">
        <!-- TODO - Remove when management page is added -->
        <div class="column is-full has-text-centered" v-if="editable">
          <router-link to="./proxies/" class="button is-success">
            <span class="icon is-small"><i class="material-icons">person_add</i></span>
            <span>Add Proxy Character</span>
          </router-link>
        </div>

        <TeamMemberCard v-for="tm in team.members" :key="tm.id" :team-id="team.id" :details="tm" :max-item-level="team.tier.max_item_level" v-on:reload="() => { fetchTeam(true) }" />
      </div>
    </template>
  </div>
</template>

<script lang="ts">
import { Component } from 'vue-property-decorator'
import TeamMemberCard from '@/components/team/member_card.vue'
import TeamNav from '@/components/team/nav.vue'
import Team from '@/interfaces/team'
import TeamMember from '@/interfaces/team_member'
import SavageAimMixin from '@/mixins/savage_aim_mixin'

@Component({
  components: {
    TeamMemberCard,
    TeamNav,
  },
})
export default class TeamView extends SavageAimMixin {
  loading = true

  team!: Team

  // Flag stating whether the currently logged user can edit the Team
  get editable(): boolean {
    return this.team.members.find((teamMember: TeamMember) => teamMember.character.user_id === this.$store.state.user.id)?.lead ?? false
  }

  get url(): string {
    return `/backend/api/team/${this.$route.params.id}/`
  }

  created(): void {
    this.fetchTeam(false)
  }

  async fetchTeam(reload: boolean): Promise<void> {
    // Load the team data from the API
    try {
      const response = await fetch(this.url)
      if (response.ok) {
        // Parse the JSON into a team and save it
        this.team = (await response.json()) as Team
        this.loading = false
        if (reload) this.$forceUpdate()
        document.title = `${this.team.name} - Savage Aim`
      }
      else {
        super.handleError(response.status)
      }
    }
    catch (e) {
      this.$notify({ text: `Error ${e} when fetching Team.`, type: 'is-danger' })
    }
  }

  async load(): Promise<void> {
    this.fetchTeam(true)
  }
}
</script>

<style lang="scss">

</style>
