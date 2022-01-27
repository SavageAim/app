<template>
  <div>
    <h2 class="title">
      Settings for {{ user.username }}
    </h2>

    <!-- Colour Scheme -->
    <div class="columns">
      <div class="column is-half">
        <div class="card">
          <div href="#" class="card-header">
            <div class="card-header-title">Colour Scheme</div>
          </div>
          <div class="card-content">
            <div class="field">
              <div class="control">
                <div class="select is-fullwidth">
                  <select v-model="theme" ref="dropdown">
                    <option value="beta">Beta</option>
                    <option value="blue">Blue</option>
                    <option value="green">Green</option>
                    <option value="purple">Purple</option>
                    <option value="red">Red</option>
                    <option value="trans">Trans Pride</option>
                  </select>
                </div>
                <p class="help is-danger" v-if="errors.theme !== undefined">{{ errors.theme[0] }}</p>
              </div>
            </div>
            <div class="divider"><i class="material-icons icon">expand_more</i> Example <i class="material-icons icon">expand_more</i></div>
            <table class="table is-bordered is-fullwidth gear-table" :class="[`is-${theme}`]">
              <tr>
                <th class="is-il-bis">Best in Slot</th>
              </tr>
              <tr>
                <th class="is-il-minus-0">Max IL - 0</th>
              </tr>
              <tr>
                <th class="is-il-minus-5">Max IL - 5</th>
              </tr>
              <tr>
                <th class="is-il-minus-10">Max IL - 10</th>
              </tr>
              <tr>
                <th class="is-il-minus-15">Max IL - 15</th>
              </tr>
              <tr>
                <th class="is-il-minus-20">Max IL - 20</th>
              </tr>
              <tr>
                <th class="is-il-minus-25">Max IL - 25</th>
              </tr>
              <tr>
                <th class="is-il-out-of-range">Out of the range of the Team's current Tier</th>
              </tr>
            </table>
          </div>
        </div>
      </div>

      <!-- Notifications -->
      <div class="column is-half">
        <div class="card">
          <a href="#" class="card-header">
            <div class="card-header-title">Notifications</div>
          </a>
          <div class="card-content">
            <p class="has-text-info">Tick or untick boxes for the Notifications you do / don't want to receive, and click save!</p>
            <hr />
            <div class="field">
              <label class="checkbox">
                <input type="checkbox" v-model="notifications.verify_success">
                Character Verification success
              </label>
            </div>
            <div class="field">
              <label class="checkbox">
                <input type="checkbox" v-model="notifications.verify_fail">
                Character Verification failed.
              </label>
            </div>
            <div class="field">
              <label class="checkbox">
                <input type="checkbox" v-model="notifications.team_lead">
                Your Character has been made leader of a Team.
              </label>
            </div>
            <div class="field">
              <label class="checkbox">
                <input type="checkbox" v-model="notifications.team_join">
                A Character has joined your team.
              </label>
            </div>
            <div class="field">
              <label class="checkbox">
                <input type="checkbox" v-model="notifications.loot_tracker_update">
                Loot Tracker updates your BIS List.
              </label>
            </div>
          </div>
        </div>
      </div>
    </div>
    <button class="button is-success is-fullwidth" @click="save">Save</button>
  </div>
</template>

<script lang="ts">
import { Component } from 'vue-property-decorator'
import { SettingsErrors } from '@/interfaces/responses'
import User from '@/interfaces/user'
import SavageAimMixin from '@/mixins/savage_aim_mixin'

@Component
export default class Settings extends SavageAimMixin {
  errors: SettingsErrors = {}

  notifications = {
    loot_tracker_update: this.user.notifications.loot_tracker_update,
    team_join: this.user.notifications.team_join,
    team_lead: this.user.notifications.team_lead,
    verify_fail: this.user.notifications.verify_fail,
    verify_success: this.user.notifications.verify_success,
  }

  theme = this.user.theme

  get dropdown(): HTMLSelectElement {
    return this.$refs.dropdown as HTMLSelectElement
  }

  mounted(): void {
    document.title = 'User Settings - Savage Aim'
  }

  // Url to send data to
  get url(): string {
    return `/backend/api/me/`
  }

  // Return the user object from the store
  get user(): User {
    return this.$store.state.user
  }

  // Save the data into a new bis list
  async save(): Promise<void> {
    const body = JSON.stringify({ theme: this.theme, notifications: this.notifications })
    try {
      const response = await fetch(this.url, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': this.$cookies.get('csrftoken'),
        },
        body,
      })

      if (response.ok) {
        // Just give a message saying it was successful
        this.$notify({ text: 'Update successful!', type: 'is-success' })
        // Update the user in the system too
        this.$store.dispatch('fetchUser')
      }
      else {
        super.handleError(response.status)
        this.errors = (await response.json() as SettingsErrors)
      }
    }
    catch (e) {
      this.$notify({ text: `Error ${e} when attempting to update User Settings.`, type: 'is-danger' })
    }
  }
}
</script>

<style lang="scss">
</style>
