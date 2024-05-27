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
            <CharacterBio :character="character" />
          </div>
          <footer class="card-footer">
            <button class="card-footer-item is-loading is-ghost button" v-if="updating"></button>
            <a class="card-footer-item" @click="updateChar" v-else>
              <span class="icon-text">
                <span class="icon"><i class="material-icons">sync</i></span>
                <span>Re-Import</span>
              </span>
            </a>
            <a class="has-text-danger card-footer-item" @click="deleteChar">
              <span class="icon-text">
                <span class="icon"><i class="material-icons">delete</i></span>
                <span>Delete</span>
              </span>
            </a>
          </footer>
        </div>

        <!-- Navigation -->
        <div class="card">
          <div class="card-content">
            <aside class="menu">
              <ul class="menu-list">
                <li><a :class="{ 'is-active': bisShown }" @click="showBIS">BIS Lists</a></li>
                <li><a :class="{ 'is-active': teamsShown }" @click="showTeams">Teams</a></li>
                <li><a :class="{ 'is-active': settingsShown }" @click="showSettings">Settings</a></li>
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
            <p>Unverified characters are now able to use the system as normal, but will be deleted in 7 days if they are not verified.</p>
            <p>Any BIS Lists they own will be deleted, and they will be removed from all Teams they are in.</p>
            <p>In order to verify, please copy the token in the box below, update <a href="https://eu.finalfantasyxiv.com/lodestone/my/setting/profile/" target="_blank">this page</a> with it, then press the "Verify Character" button.</p>
            <hr />
            <div class="field has-addons">
              <div class="control is-expanded">
                <input class="input is-link" id="characterToken" type="text" :value="character.token" readonly />
              </div>
              <label class="label is-sr-only" for="characterToken">Character Verification Token</label>
              <div class="control">
                <button class="button is-link" @click="verify">Verify Character</button>
              </div>
            </div>
          </div>
        </article>

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
                <router-link to="./bis_list/" class="button is-success">
                  <span class="icon"><i class="material-icons">add</i></span>
                  <span>Add New</span>
                </router-link>
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
                  <img :src="`/job_icons/${bis.job.id}.webp`" :alt="`${bis.job.name} job icon`" width="24" height="24" />
                </span>
              </div>
            </div>
            <div class="card-content">
              <BISTable :list="bis" />
              <p class="has-text-info has-text-centered bis-colour-info">Colours generated using item level {{ bis.bis_mainhand.item_level }}</p>
            </div>
            <!-- Dropdown for mobile -->
            <footer class="card-footer is-hidden-desktop">
              <div class="dropdown is-centered card-footer-item" :class="{'is-active': actionsActive[bis.id] || false}">
                <div class="dropdown-trigger">
                  <a class="icon-text" aria-haspopup="true" :aria-controls="`actions-${bis.id}`" @click="() => { toggleActions(bis.id) }">
                    <span class="icon"><i class="material-icons">more_vert</i></span>
                    <span>Actions</span>
                    <span class="icon">
                      <i class="material-icons" v-if="actionsActive[bis.id]">expand_less</i>
                      <i class="material-icons" v-else>expand_more</i>
                    </span>
                  </a>
                </div>
                <div class="dropdown-menu" :id="`actions-${bis.id}`" role="menu">
                  <div class="dropdown-content">
                    <template v-if="bis.external_link != null">
                      <a target="_blank" :href="bis.external_link" class="card-footer-item">
                        <span class="icon-text">
                          <span class="icon"><i class="material-icons">open_in_new</i></span>
                          <span>{{ bis.external_link.replace(/https?:\/\//, '').split('/')[0] }}</span>
                        </span>
                      </a>
                      <hr class="dropdown-divider" />
                    </template>
                    <router-link :to="`/characters/${character.id}/bis_list/${bis.id}/`" class="card-footer-item">
                      <span class="icon-text">
                        <span class="icon"><i class="material-icons">edit</i></span>
                        <span>Edit BIS</span>
                      </span>
                    </router-link>
                    <hr class="dropdown-divider" />
                    <!-- clone BIS -->
                    <a class="card-footer-item" @click="() => { duplicateBIS(bis) }">
                      <span class="icon-text">
                        <span class="icon"><i class="material-icons">copy_all</i></span>
                        <span>Copy</span>
                      </span>
                    </a>
                    <hr class="dropdown-divider" />
                    <!-- Modal to confirm, Delete BIS -->
                    <a class="card-footer-item has-text-danger" @click="() => { deleteBIS(bis) }">
                      <span class="icon-text">
                        <span class="icon"><i class="material-icons">delete</i></span>
                        <span>Delete BIS</span>
                      </span>
                    </a>
                  </div>
                </div>
              </div>
            </footer>

            <!-- No Dropdown for Desktop -->
            <footer class="card-footer has-text-link is-hidden-touch">
              <a target="_blank" :href="bis.external_link" class="card-footer-item" v-if="bis.external_link != null">
                <span class="icon-text">
                  <span class="icon"><i class="material-icons">open_in_new</i></span>
                  <span>{{ bis.external_link.replace(/https?:\/\//, '').split('/')[0] }}</span>
                </span>
              </a>
              <!-- Quick link to edit this bis list -->
              <router-link :to="`/characters/${character.id}/bis_list/${bis.id}/`" class="card-footer-item">
                <span class="icon-text">
                  <span class="icon"><i class="material-icons">edit</i></span>
                  <span>Edit BIS</span>
                </span>
              </router-link>
              <!-- clone BIS -->
              <a class="card-footer-item" @click="() => { duplicateBIS(bis) }">
                <span class="icon-text">
                  <span class="icon"><i class="material-icons">copy_all</i></span>
                  <span>Copy</span>
                </span>
              </a>
              <!-- Modal to confirm, delete BIS -->
              <a class="card-footer-item has-text-danger" @click="() => { deleteBIS(bis) }">
                <span class="icon-text">
                  <span class="icon"><i class="material-icons">delete</i></span>
                  <span>Delete BIS</span>
                </span>
              </a>
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
                <router-link to="/team/" class="button is-success">
                  <span class="icon"><i class="material-icons">add</i></span>
                  <span>Add New</span>
                </router-link>
              </div>
            </div>
          </div>
          <div class="card" v-if="teams.length">
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
              <a class="has-text-success card-footer-item" @click="saveDetails">
                <span class="icon-text">
                  <span class="icon"><i class="material-icons">save</i></span>
                  <span>Save Settings</span>
                </span>
              </a>
            </footer>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import * as Sentry from '@sentry/vue'
import { Component, Prop } from 'vue-property-decorator'
import BISTable from '@/components/bis_table.vue'
import CharacterBio from '@/components/character_bio.vue'
import DeleteBIS from '@/components/modals/confirmations/delete_bis.vue'
import DeleteCharacter from '@/components/modals/confirmations/delete_character.vue'
import TeamBio from '@/components/team/bio.vue'
import BISListModify from '@/dataclasses/bis_list_modify'
import BISList from '@/interfaces/bis_list'
import { CharacterDetails } from '@/interfaces/character'
import Job from '@/interfaces/job'
import { CharacterScrapeData, CharacterScrapeError } from '@/interfaces/lodestone'
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
  actionsActive: { [bisId: number]: boolean } = {}

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

  get bisListUrl(): string {
    return `/backend/api/character/${this.characterId}/bis_lists/`
  }

  get lodestoneUrl(): string {
    return `/backend/api/lodestone/${this.character.lodestone_id}/`
  }

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

  async duplicateBIS(bis: BISList): Promise<void> {
    // Create a shallow copy of the bis list, change the name and send a post request to the endpoint
    const dupedBis = BISListModify.buildEditVersion(bis)
    dupedBis.name = `Copy of ${bis.display_name}`
    try {
      const response = await fetch(this.bisListUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': this.$cookies.get('csrftoken'),
        },
        body: JSON.stringify(dupedBis),
      })

      if (response.ok) {
        this.$notify({ text: 'BIS List copied successfully!', type: 'is-success' })
      }
      else {
        this.$notify({ text: 'BIS List could not be copied.', type: 'is-danger' })
      }
    }
    catch (e) {
      this.$notify({ text: `Error ${e} when attempting to create BIS List.`, type: 'is-danger' })
      Sentry.captureException(e)
    }
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
      Sentry.captureException(e)
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
      Sentry.captureException(e)
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
      Sentry.captureException(e)
    }
  }

  toggleActions(bisId: number): void {
    this.actionsActive[bisId] = !(this.actionsActive[bisId] || false)
    this.$forceUpdate()
  }

  async updateChar(): Promise<void> {
    if (this.updating) return

    this.updating = true
    // Reload data from the Lodestone, and send an update request to the API.
    // We just need to update the name, world, and image url
    try {
      const response = await fetch(this.lodestoneUrl, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': this.$cookies.get('csrftoken'),
        },
      })
      if (response.ok) {
        const json = await response.json() as CharacterScrapeData
        // Update the local character and use the same function for updating alias
        this.character.avatar_url = json.avatar_url
        this.character.name = json.name
        this.character.world = `${json.world} (${json.dc})`
        await this.saveDetails()
      }
      else {
        const json = await response.json() as CharacterScrapeError
        this.$notify({ text: `Received error when attempting to update Character details from Lodestone; ${json.message}`, type: 'is-danger' })
      }
    }
    catch (err) {
      this.$notify({ text: `Unexpected error ${err} when attempting to update Character details.`, type: 'is-danger' })
      Sentry.captureException(err)
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
        this.$notify({ text: 'Verification requested, please wait!', type: 'is-success' })
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
      this.$notify({ text: `Error ${e} when attempting to add Character to verification queue.`, type: 'is-danger' })
      Sentry.captureException(e)
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

p.bis-colour-info {
  margin-top: 1rem;
}
</style>
