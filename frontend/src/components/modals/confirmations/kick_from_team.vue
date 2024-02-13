<template>
  <div>
    <div class="card-header">
      <div class="card-header-title">Are you sure you want to kick this Character?</div>
      <div class="card-header-icon">
        <a @click="() => { this.$emit('close') }" class="icon">
          <i class="material-icons">close</i>
        </a>
      </div>
    </div>
    <div class="card-content">
      <div class="box">
        <div class="level is-mobile">
          <div class="level-left">
            <div class="level-item">
              <span class="icon is-hidden-touch" v-if="details.character.proxy"><img src="/proxy.png" alt="Proxy Character" title="Proxy Character" width="24" height="24" /></span>
              <span class="icon is-hidden-touch" v-else><img src="/party_member.png" alt="Team Member" title="Team Member" width="24" height="24" /></span>
              <span>{{ details.name }}</span>
            </div>
          </div>
          <div class="level-right">
            <div class="level-item">
              <span class="tags has-addons">
                <span class="tag is-light">
                  iL
                </span>
                <span class="tag" :class="[`is-${details.bis_list.job.role}`]">
                  {{ details.bis_list.item_level }}
                </span>
              </span>
            </div>
            <div class="level-item">
              <span class="icon">
                <img :src="`/job_icons/${details.bis_list.job.id}.png`" :alt="`${details.bis_list.job.name} job icon`" width="24" height="24" />
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="card-footer">
      <a class="card-footer-item has-text-danger" @click="kickFromTeam">
        <span class="icon-text">
          <span class="icon"><i class="material-icons">delete</i></span>
          <span>Kick</span>
        </span></a>
      <a class="card-footer-item has-text-link" @click="() => { this.$emit('close') }">
        <span class="icon-text">
          <span class="icon"><i class="material-icons">close</i></span>
          <span>Cancel</span>
        </span>
      </a>
    </div>
  </div>
</template>

<script lang="ts">
import * as Sentry from '@sentry/vue'
import { Component, Prop, Vue } from 'vue-property-decorator'
import TeamMember from '@/interfaces/team_member'

@Component
export default class KickFromTeam extends Vue {
  @Prop()
  details!: TeamMember

  @Prop()
  teamId!: number

  get url(): string {
    return `/backend/api/team/${this.teamId}/member/${this.details.id}/`
  }

  async kickFromTeam(): Promise<void> {
    try {
      const response = await fetch(this.url, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': Vue.$cookies.get('csrftoken'),
        },
      })

      if (response.ok) {
        // Attempt to parse the json, get the id, and then redirect
        this.$store.dispatch('fetchTeams')
        this.$emit('close')
        this.$notify({ text: `Successfully kicked ${this.details.character.name} @ ${this.details.character.world} from the Team!`, type: 'is-success' })
      }
      else {
        this.$notify({ text: `Unexpected response ${response.status} when attempting to kick Team Member.`, type: 'is-danger' })
      }
    }
    catch (e) {
      this.$notify({ text: `Error ${e} when attempting to kick Team Member.`, type: 'is-danger' })
      Sentry.captureException(e)
    }
  }
}
</script>
