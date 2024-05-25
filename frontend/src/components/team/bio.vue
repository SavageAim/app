<template>
  <div>
    <article class="media">
      <div class="media-left is-hidden-mobile">
        <div class="icon" v-if="displayIcons">
          <img v-if="isLead()" src="/party_lead.webp" alt="Team Leader" width="32" height="32" />
          <img v-else src="/party_member.webp" alt="Team Member" width="32" height="32" />
        </div>
      </div>
      <div class="media-content">
        <p class="title is-4">{{ team.name }}</p>
        <div class="icon-text subtitle">
          <span class="icon"><i class="material-icons">room</i></span>
          <span>{{ team.tier.name }}</span>
        </div>
      </div>
    </article>
    <div class="level is-hidden-mobile">
      <div v-for="member in team.members" :key="member.id" class="level-item">
        <span class="icon" data-microtip-position="top" role="tooltip" :aria-label="member.name">
          <img :src="`/job_icons/${member.bis_list.job.id}.webp`" :alt="`${member.bis_list.job.display_name} Job Icon`" height="24" width="24" />
        </span>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'
import Team from '@/interfaces/team'
import TeamMember from '@/interfaces/team_member'

@Component
export default class TeamBio extends Vue {
  @Prop({ default: true })
  displayIcons!: boolean

  @Prop()
  team!: Team

  // Check if the requesting user is the leader of the given team
  isLead(): boolean {
    // Check for the member that is owned by the requesting user and return the value of the lead property
    return this.team.members.find((teamMember: TeamMember) => teamMember.character.user_id === this.$store.state.user.id)?.lead ?? false
  }
}
</script>

<style lang="scss">
</style>
