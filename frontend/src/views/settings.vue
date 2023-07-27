<template>
  <div>
    <h2 class="title">
      Settings for {{ user.username }}
    </h2>

    <!-- Colour Scheme -->
    <div class="columns">
      <div class="column is-half">
        <ThemeSettings
          :errors="errors"
          :theme="theme"
          v-on:changeTheme="changeTheme"
        />
      </div>

      <!-- Notifications -->
      <div class="column is-half">
        <NotificationsSettings
          :errors="errors"
          :notifications="notifications"
          v-on:changeNotification="changeNotification"
        />
      </div>
    </div>
    <button class="button is-success is-fullwidth" @click="save">Save</button>
  </div>
</template>

<script lang="ts">
import { Component, Watch } from 'vue-property-decorator'
import NotificationsSettings from '@/components/settings/notifications.vue'
import ThemeSettings from '@/components/settings/theme.vue'
import NotificationSettings from '@/interfaces/notification_settings'
import { SettingsErrors } from '@/interfaces/responses'
import User from '@/interfaces/user'
import SavageAimMixin from '@/mixins/savage_aim_mixin'

@Component({
  components: {
    NotificationsSettings,
    ThemeSettings,
  },
})
export default class Settings extends SavageAimMixin {
  errors: SettingsErrors = {}

  notifications = {
    ...this.user.notifications,
  }

  theme = this.user.theme

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

  changeNotification(data: {notification: keyof NotificationSettings, value: boolean}): void {
    this.notifications[data.notification] = data.value
  }

  changeTheme(theme: string): void {
    this.theme = theme
  }

  // Function called on page reload via websockets
  async load(): Promise<void> {
    // This function does nothing on purpose
  }

  // Reset the settings when the User changes
  @Watch('$store.state.user', { deep: true })
  reset(): void {
    this.theme = this.$store.state.user.theme
    this.notifications = { ...this.$store.state.user.notifications }
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
