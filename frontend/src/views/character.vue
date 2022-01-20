<template>
  <div id="new-char" class="container">
    <div v-if="loading">
      <button class="button is-static is-loading is-fullwidth">Loading</button>
    </div>
    <div v-else class="columns">
      <!-- Character Display -->
      <div class="column is-one-quarter-desktop">
        <div class="card">
          <div class="card-content">
            <CharacterBio :character="character" :displayUnverified="false" />
          </div>
          <!-- <footer class="card-footer">
            <button class="button is-fullwidth is-danger is-outlined" @click="deleteChar">Delete Character</button>
          </footer> -->
        </div>
      </div>

      <!-- Lists -->
      <div class="column">
        <!-- Unverified notice -->
        <article class="message is-warning" v-if="!character.verified">
          <div class="message-header">
            <div class="icon-text">
              <span class="icon"><i class="material-icons">warning</i></span>
              <span>Unverified Character</span>
            </div>
          </div>
          <div class="message-body">
            <p>Please be aware that this character is yet to be verified.</p>
            <p>Unverified characters cannot create gear lists, or interact with teams.</p>
            <p>In order to verify, please copy the token below the line, and update <a href="https://eu.finalfantasyxiv.com/lodestone/my/setting/profile/" target="_blank">this page</a> with it, then press the "Request Verification" button.</p>
            <p>Unverified characters are removed from the system after 24h.</p>
            <hr />
            <p class="has-text-centered has-text-link">{{ character.token }}</p>
            <div class="buttons is-centered">
              <button class="button is-outlined is-link" @click="verify">Request Verification</button>
            </div>
          </div>
        </article>

        <template v-else>
          <!-- BIS Lists -->
          <div class="card">
            <div class="card-content">
              <div class="level">
                <div class="level-left">
                  <div class="level-item">
                    <h2 class="title">BIS Lists</h2>
                  </div>
                </div>
                <div class="level-right">
                  <div class="level-item">
                    <router-link to="./bis_list/" class="button is-info">Add New</router-link>
                  </div>
                </div>
              </div>
              <router-link class="box" :to="`./bis_list/${list.id}/`" v-for="list in character.bis_lists" :key="list.id">
                <div class="level">
                  <div class="level-left">
                    <div class="level-item">
                      <span class="icon-text">
                        <span class="icon"><img :src="`/job_icons/${list.job.name}.png`" :alt="`${list.job.display_name} Job Icon`" /></span>
                        <span>{{ list.job.display_name }}</span>
                      </span>
                    </div>
                  </div>
                  <div class="level-right">
                    <div class="level-item">
                      <div class="tags has-addons">
                        <span class="tag is-light">
                          iL
                        </span>
                        <span class="tag" :class="[`is-${list.job.role}`]">
                          {{ list.item_level }}
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              </router-link>
            </div>
          </div>

          <!-- Teams -->
          <div class="card">
            <div class="card-content">
              <div class="level">
                <div class="level-left">
                  <div class="level-item">
                    <h2 class="title">Teams</h2>
                  </div>
                </div>
                <div class="level-right">
                  <div class="level-item">
                    <router-link to="/team/" class="button is-info">Add New</router-link>
                  </div>
                </div>
              </div>
              <router-link class="box" :to="`/team/${team.id}/`" v-for="team in teams" :key="team.id" :set="job = getJob(team)">
                <div class="level">
                  <div class="level-left">
                    <div class="level-item">
                      <h2 class="title is-4">{{ team.name }}</h2>
                    </div>
                  </div>
                  <div class="level-right">
                    <div class="level-item">
                      <span class="icon-text">
                        <span class="icon"><img :src="`/job_icons/${job.name}.png`" :alt="`${job.display_name} Job Icon`" /></span>
                      </span>
                    </div>
                  </div>
                </div>
              </router-link>
            </div>
          </div>
        </template>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component } from 'vue-property-decorator'
import { CharacterDetails } from '@/interfaces/character'
import Job from '@/interfaces/job'
import Team from '@/interfaces/team'
import TeamMember from '@/interfaces/team_member'
import SavageAimMixin from '@/mixins/savage_aim_mixin'
import CharacterBio from '@/components/character_bio.vue'
import ConfirmDelete from '@/components/modals/confirm_delete.vue'

@Component({
  components: {
    CharacterBio,
  },
})
export default class Character extends SavageAimMixin {
  character!: CharacterDetails

  teams: Team[] = []

  loading = true

  get url(): string {
    return `/backend/api/character/${this.$route.params.id}/`
  }

  get teamsUrl(): string {
    return `/backend/api/team/?char_id=${this.$route.params.id}`
  }

  created(): void {
    this.fetchChar()
    this.fetchTeams()
  }

  async deleteChar(): Promise<void> {
    // Prompt deletion first before sending an api request (we'll use a modal instead of javascript alerts)
    this.$modal.show(ConfirmDelete, { character: this.character })
  }

  async fetchChar(): Promise<void> {
    // Load the character data from the API
    try {
      const response = await fetch(this.url)
      if (response.ok) {
        // Parse the list into an array of character interfaces and store them in the character data list
        this.character = (await response.json()) as CharacterDetails
        this.loading = false
        document.title = `${this.character.name} @ ${this.character.world} - Savage Aim`
      }
      else {
        super.handleError(response.status)
      }
    }
    catch (e) {
      this.$notify({ text: `Error ${e} when fetching Character.`, type: 'is-danger' })
    }
  }

  async fetchTeams(): Promise<void> {
    // Load the character data from the API
    try {
      const response = await fetch(this.teamsUrl)
      if (response.ok) {
        // Parse the list into an array of teams and store them in the teams data list
        this.teams = (await response.json()) as Team[]
      }
      else {
        super.handleError(response.status)
      }
    }
    catch (e) {
      this.$notify({ text: `Error ${e} when fetching Character's Team List.`, type: 'is-danger' })
    }
  }

  // Return the details of the Job the character plays in the given Team
  getJob(team: Team): Job {
    return team.members.find((tm: TeamMember) => tm.character.id === parseInt(this.$route.params.id, 10))!.bis_list.job
  }

  async verify(): Promise<void> {
    // Send a verification request to the API. Since it's a celery based system, there's no need to reload
    if (this.character.verified) return // No need running this function if we're already verified

    try {
      const response = await fetch(`${this.url}verify/`, {
        credentials: 'include',
        method: 'POST',
        headers: {
          'X-CSRFToken': this.$cookies.get('csrftoken'),
        },
      })
      if (response.ok) {
        this.$notify({ text: 'Verification requested, please check back in a few minutes!', type: 'is-success' })
      }
      else {
        this.$notify({ text: `Unexpected HTTP status ${response.status} received when attempting to add Character to verification queue.`, type: 'is-danger' })
      }
    }
    catch (e) {
      this.$notify({ text: `Error ${e} when attempting to add Character to verification queue..`, type: 'is-danger' })
    }
  }
}
</script>

<style lang="scss">
</style>
