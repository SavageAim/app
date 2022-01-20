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
            <TeamNav :editable="editable" />
          </div>
        </div>
      </div>

      <div class="columns is-multiline is-desktop">
        <TeamMemberCard v-for="tm in team.members" :key="tm.id" :details="tm" :max-item-level="team.tier.max_item_level" :editable="editable" />
      </div>
    </template>
  </div>
</template>

<script lang="ts">
import { Component } from 'vue-property-decorator'
import TeamMemberCard from '@/components/team_member_card.vue'
import TeamNav from '@/components/team_nav.vue'
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
    this.fetchTeam()
  }

  async fetchTeam(): Promise<void> {
    // Load the team data from the API
    try {
      const response = await fetch(this.url)
      if (response.ok) {
        // Parse the JSON into a team and save it
        this.team = (await response.json()) as Team
        this.loading = false
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
}
</script>

<style lang="scss">
.card-header-icon {
  cursor: default;
}

.card-header-icon > :not(:last-child) {
  margin-right: 0.5rem;
}

.card-header-icon .tags {
  margin-bottom: 0;

  & .tag {
    margin-bottom: 0;
  }
}
</style>
