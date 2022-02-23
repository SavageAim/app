<template>
  <div>
    <div class="card-header">
      <div class="card-header-title"></div>
      <div class="card-header-icon">
        <a @click="() => { this.$emit('close') }" class="icon">
          <i class="material-icons">close</i>
        </a>
      </div>
    </div>
    <div class="card-content">
      <h2 class="subtitle">Are you sure you want to disband this Team?</h2>
      <hr />
      <div class="box">
        <TeamBio :team="team" />
      </div>
      <hr />
      <p>Please type <code>{{ team.name }}</code> to confirm.</p>
      <input class="input" v-model="input" />
    </div>
    <div class="card-footer">
      <a class="card-footer-item" @click="() => { this.$emit('close') }">Cancel</a>
      <a class="card-footer-item has-text-danger" v-if="canDelete" @click="deleteTeam">Disband</a>
      <p class="card-footer-item disabled-delete" v-else data-microtip-position="top" role="tooltip" aria-label="Please confirm deletion.">Disband</p>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'
import TeamBio from '@/components/team_bio.vue'
import Team from '@/interfaces/team'

@Component({
  components: {
    TeamBio,
  },
})
export default class DeleteTeam extends Vue {
  @Prop()
  team!: Team

  input = ''

  get canDelete(): boolean {
    return this.input === this.team.name
  }

  get url(): string {
    return `/backend/api/team/${this.team.id}/`
  }

  async deleteTeam(): Promise<void> {
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
        this.$router.push('/', () => {
          Vue.notify({ text: `${this.team.name} disbanded successfully!`, type: 'is-success' })
        })
      }
      else {
        this.$notify({ text: `Unexpected response ${response.status} when attempting to disband ${this.team.name}.`, type: 'is-danger' })
      }
    }
    catch (e) {
      this.$notify({ text: `Error ${e} when attempting to disband ${this.team.name}.`, type: 'is-danger' })
    }
  }
}
</script>
