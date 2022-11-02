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
          <footer class="card-footer">
            <button class="card-footer-item is-loading is-ghost button" v-if="updating"></button>
            <a class="card-footer-item" @click="updateChar" v-else>Update</a>
            <a class="has-text-danger card-footer-item" @click="deleteChar">Delete</a>
          </footer>
        </div>

        <!-- Navigation -->
        <div class="card" v-if="character.verified">
          <div class="card-content">
            <aside class="menu">
              <ul class="menu-list">
                <li><a :class="{ 'is-active': bisShown }" @click="showBIS">View BIS Lists</a></li>
                <li><a :class="{ 'is-active': teamsShown }" @click="showTeams">View Teams</a></li>
                <li><a :class="{ 'is-active': settingsShown }" @click="showSettings">View Settings</a></li>
              </ul>
            </aside>
          </div>
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
          <div v-if="bisShown">
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

            <div class="card" v-for="bis in character.bis_lists" :key="bis.id">
              <div class="card-header">
                <div class="card-header-title">
                  <span>{{ bis.display_name }}</span>
                </div>
                <div class="card-header-icon">
                  <div class="tags has-addons is-hidden-touch">
                    <span class="tag is-light">
                      iL
                    </span>
                    <span class="tag" :class="[`is-${bis.job.role}`]">
                      {{ bis.item_level }}
                    </span>
                  </div>
                  <span class="icon">
                    <img :src="`/job_icons/${bis.job.id}.png`" :alt="`${bis.job.name} job icon`" width="24" height="24" />
                  </span>
                </div>
              </div>
              <div class="card-content">
                <BISTable :list="bis" />
                <p class="has-text-info has-text-centered">Colours generated using item level {{ bis.bis_mainhand.item_level }}</p>
              </div>
              <footer class="card-footer">
                <router-link :to="`/characters/${character.id}/bis_list/${bis.id}/`" class="card-footer-item">
                  Edit
                </router-link>
                <a v-if="bis.external_link != null" target="_blank" :href="bis.external_link" class="card-footer-item">
                  View on {{ bis.external_link.replace(/https?:\/\//, '').split('/')[0] }}
                </a>
                <a class="has-text-danger card-footer-item" @click="() => { deleteBIS(bis) }">Delete</a>
              </footer>
            </div>
            <div class="subtitle has-text-centered" v-if="character.bis_lists.length === 0">
              <p>No BIS Lists here yet!</p>
            </div>
          </div>

          <!-- Teams -->
          <div v-if="teamsShown">
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
            <div class="card">
              <div class="card-content">
                <router-link class="box" :to="`/team/${team.id}/`" v-for="team in teams" :key="team.id" :set="job = getJob(team)">
                  <TeamBio :team="team" />
                </router-link>
              </div>
            </div>
            <div class="subtitle has-text-centered" v-if="teams.length === 0">
              <p>No Teams here yet!</p>
            </div>
          </div>

          <!-- Settings -->
          <div v-if="settingsShown">
            <div class="level">
              <div class="level-left">
                <div class="level-item">
                  <h2 class="title">Settings</h2>
                </div>
              </div>
            </div>
            <div class="card">
              <div class="card-content">
                <div class="field">
                  <label class="label" for="alias">Alias</label>
                  <div class="control">
                    <input class="input" id="alias" type="text" placeholder="Alias" v-model="character.alias" :class="{'is-danger': errors.alias !== undefined}" />
                  </div>
                  <p v-if="errors.alias !== undefined" class="help is-danger">{{ errors.alias[0] }}</p>
                </div>
              </div>
              <footer class="card-footer">
                <a class="has-text-success card-footer-item" @click="saveDetails">Save</a>
              </footer>
            </div>
          </div>
        </template>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop } from 'vue-property-decorator'
import XIVAPI from '@xivapi/js'
import BISTable from '@/components/bis_table.vue'
import CharacterBio from '@/components/character_bio.vue'
import DeleteBIS from '@/components/modals/confirmations/delete_bis.vue'
import DeleteCharacter from '@/components/modals/confirmations/delete_character.vue'
import TeamBio from '@/components/team/bio.vue'
import BISList from '@/interfaces/bis_list'
import { CharacterDetails } from '@/interfaces/character'
import Job from '@/interfaces/job'
import { CharacterUpdateErrors } from '@/interfaces/responses'
import Team from '@/interfaces/team'
import TeamMember from '@/interfaces/team_member'
import SavageAimMixin from '@/mixins/savage_aim_mixin'

@Component({
  components: {
    BISTable,
    CharacterBio,
    TeamBio,
  },
})
export default class Character extends SavageAimMixin {
  bisShown = true

  character!: CharacterDetails

  @Prop()
  characterId!: string

  errors: CharacterUpdateErrors = {}

  settingsShown = false

  teams: Team[] = []

  teamsShown = false

  loading = true

  updating = false

  get teamsUrl(): string {
    return `/backend/api/team/?char_id=${this.characterId}`
  }

  get url(): string {
    return `/backend/api/character/${this.characterId}/`
  }

  created(): void {
    this.fetchChar(false)
    this.fetchTeams()
  }

  deleteBIS(bis: BISList): void {
    // Prompt deletion first before sending an api request (we'll use a modal instead of javascript alerts)
    const { path } = this.$route // Store the path we were on so if the modal navigates off we don't try to run bad code
    this.$modal.show(DeleteBIS, { bis, character: this.character }, { }, { closed: () => { if (this.$route.path === path) this.fetchChar(true) } })
  }

  deleteChar(): void {
    // Prompt deletion first before sending an api request (we'll use a modal instead of javascript alerts)
    this.$modal.show(DeleteCharacter, { character: this.character })
  }

  async fetchChar(reload: boolean): Promise<void> {
    // Load the character data from the API
    try {
      const response = await fetch(this.url)
      if (response.ok) {
        // Parse the list into an array of character interfaces and store them in the character data list
        this.character = (await response.json()) as CharacterDetails
        this.loading = false
        if (reload) this.$forceUpdate()
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
    return team.members.find((tm: TeamMember) => tm.character.id === parseInt(this.characterId, 10))!.bis_list.job
  }

  // WS reload
  async load(): Promise<void> {
    this.fetchChar(true)
    this.fetchTeams()
  }

  async saveDetails(): Promise<void> {
    // Update fields for the Character
    this.errors = {}
    const body = JSON.stringify(this.character)
    try {
      const response = await fetch(this.url, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': this.$cookies.get('csrftoken'),
        },
        body,
      })

      if (response.ok) {
        this.$notify({ text: 'Successfully updated!', type: 'is-success' })
        this.$forceUpdate()
      }
      else {
        super.handleError(response.status)
        this.errors = (await response.json() as CharacterUpdateErrors)
      }
    }
    catch (e) {
      this.$notify({ text: `Error ${e} when attempting to update Character.`, type: 'is-danger' })
    }
  }

  async updateChar(): Promise<void> {
    if (!this.character.verified || this.updating) return

    this.updating = true
    // Reload data from the Lodestone, and send an update request to the API.
    // We just need to update the name, world, and image url
    const xiv = new XIVAPI()
    try {
      const response = (await xiv.character.get(this.character.lodestone_id))
      // Update the local character and use the same function for updating alias
      this.character.avatar_url = response.Character.Avatar
      this.character.name = response.Character.Name
      this.character.world = `${response.Character.Server} (${response.Character.DC})`
      await this.saveDetails()
    }
    catch (err) {
      let errorMessage: string
      if (err.error != null) {
        // XIVAPI Error
        errorMessage = err.error.Message
      }
      else {
        // Normal JS error
        errorMessage = err.message
      }
      this.$notify({ text: `Received error when attempting to update Character details from Lodestone; ${errorMessage}`, type: 'is-danger' })
    }
    finally {
      this.updating = false
    }
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
      else if (response.status === 404) {
        // Status 404 on this page likely means the character is verified
        this.fetchChar(true)
      }
      else {
        this.$notify({ text: `Unexpected HTTP status ${response.status} received when attempting to add Character to verification queue.`, type: 'is-danger' })
      }
    }
    catch (e) {
      this.$notify({ text: `Error ${e} when attempting to add Character to verification queue..`, type: 'is-danger' })
    }
  }

  // Show code for the tabs
  showBIS(): void {
    this.showNone()
    this.bisShown = true
  }

  showNone(): void {
    this.bisShown = false
    this.settingsShown = false
    this.teamsShown = false
  }

  showSettings(): void {
    this.showNone()
    this.settingsShown = true
  }

  showTeams(): void {
    this.showNone()
    this.teamsShown = true
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

button.is-loading.is-ghost {
  // Fixing a slight centering issue
  margin-top: 4px;
}
</style>
