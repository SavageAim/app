<template>
  <div>
    <!-- Navigation -->
    <div class="columns">
      <div class="column is-one-quarter-desktop">
        <div class="card">
          <div class="card-header">
            <div class="card-header-title">User Settings</div>
          </div>
          <div class="card-content">
            <aside class="menu">
              <ul class="menu-list">
              <li>
                  <a :class="{ 'is-active': activeTab.details, 'has-text-danger': errorsInDetails() }" @click="showDetails">
                    User Details <span v-if="unsavedDetails()">*</span>
                  </a>
                </li>
                <li>
                  <a :class="{ 'is-active': activeTab.theme, 'has-text-danger': errorsInTheme() }" @click="showTheme">
                    Colour Scheme <span v-if="unsavedTheme()">*</span>
                  </a>
                </li>
                <li>
                  <a :class="{ 'is-active': activeTab.notifications, 'has-text-danger': errorsInNotifications() }" @click="showNotifications">
                    Notifications <span v-if="unsavedNotifications()">*</span>
                  </a>
                </li>
                <li>
                  <a :class="{ 'is-active': activeTab.lootManager, 'has-text-danger': errorsInLootManager() }" @click="showLootManager">
                    Loot Manager Version <span v-if="unsavedLootManager()">*</span>
                  </a>
                </li>
              </ul>
            </aside>
          </div>
        </div>
        <button class="button is-success is-fullwidth" @click="save">
          <span class="icon"><i class="material-icons">save</i></span>
          <span>Save</span>
        </button>
      </div>

      <!-- Notifications -->
      <div class="column">
        <UserDetailsSettings
          :errors="errors"
          :token="token"
          :username="username"
          v-on:changeUsername="changeUsername"
          v-if="activeTab.details"
        />
        <!-- Colour Scheme -->
        <ThemeSettings
          :errors="errors"
          :theme="theme"
          v-on:changeTheme="changeTheme"
          v-if="activeTab.theme"
        />
        <NotificationsSettingsComponent
          :notifications="notifications"
          v-on:changeNotification="changeNotification"
          v-if="activeTab.notifications"
        />
        <LootManagerSettings
          :errors="errors"
          :loot-manager-version="lootManagerVersion"
          v-on:changeLootManagerVersion="changeLootManagerVersion"
          v-if="activeTab.lootManager"
        />
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import isEqual from 'lodash.isequal'
import * as Sentry from '@sentry/vue'
import { Component, Watch } from 'vue-property-decorator'
import LootManagerSettings from '@/components/settings/loot_manager.vue'
import NotificationsSettingsComponent from '@/components/settings/notifications.vue'
import ThemeSettings from '@/components/settings/theme.vue'
import UserDetailsSettings from '@/components/settings/user_details.vue'
import NotificationSettings from '@/interfaces/notification_settings'
import { SettingsErrors } from '@/interfaces/responses'
import User from '@/interfaces/user'
import SavageAimMixin from '@/mixins/savage_aim_mixin'

@Component({
  components: {
    LootManagerSettings,
    NotificationsSettingsComponent,
    ThemeSettings,
    UserDetailsSettings,
  },
})
export default class Settings extends SavageAimMixin {
  activeTab = {
    details: true,
    theme: false,
    notifications: false,
    lootManager: false,
  }

  errors: SettingsErrors = {}

  lootManagerVersion = this.user.loot_manager_version

  notifications = {
    ...this.user.notifications,
  }

  token = this.user.token

  theme = this.user.theme

  username = this.user.username

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

  changeLootManagerVersion(version: string): void {
    this.lootManagerVersion = version
  }

  changeNotification(data: {notification: keyof NotificationSettings, value: boolean}): void {
    this.notifications[data.notification] = data.value
  }

  changeTheme(theme: string): void {
    this.theme = theme
  }

  changeUsername(username: string): void {
    this.username = username
  }

  errorsInDetails(): boolean {
    return (this.errors.username?.length || 0) > 0
  }

  errorsInLootManager(): boolean {
    return (this.errors.loot_manager_version?.length || 0) > 0
  }

  errorsInNotifications(): boolean {
    return (this.errors.notifications?.length || 0) > 0
  }

  errorsInTheme(): boolean {
    return (this.errors.theme?.length || 0) > 0
  }

  // Function called on page reload via websockets
  async load(): Promise<void> {
    // This function does nothing on purpose
  }

  // Reset the settings when the User changes
  @Watch('$store.state.user', { deep: true })
  reset(): void {
    this.token = this.$store.state.user.token
    this.theme = this.$store.state.user.theme
    this.notifications = { ...this.$store.state.user.notifications }
  }

  resetActiveTab(): void {
    this.activeTab.details = false
    this.activeTab.theme = false
    this.activeTab.notifications = false
    this.activeTab.lootManager = false
  }

  // Save the data into a new bis list
  async save(): Promise<void> {
    const body = JSON.stringify({
      theme: this.theme,
      notifications: this.notifications,
      loot_manager_version: this.lootManagerVersion,
      username: this.username,
    })

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
        // Reset Errors
        this.errors = {}
      }
      else {
        super.handleError(response.status)
        this.errors = (await response.json() as SettingsErrors)
      }
    }
    catch (e) {
      this.$notify({ text: `Error ${e} when attempting to update User Settings.`, type: 'is-danger' })
      Sentry.captureException(e)
    }
  }

  showDetails(): void {
    this.resetActiveTab()
    this.activeTab.details = true
  }

  showLootManager(): void {
    this.resetActiveTab()
    this.activeTab.lootManager = true
  }

  showNotifications(): void {
    this.resetActiveTab()
    this.activeTab.notifications = true
  }

  showTheme(): void {
    this.resetActiveTab()
    this.activeTab.theme = true
  }

  unsavedDetails(): boolean {
    return this.username !== this.user.username
  }

  unsavedLootManager(): boolean {
    return this.lootManagerVersion !== this.user.loot_manager_version
  }

  unsavedNotifications(): boolean {
    return !isEqual(this.notifications, this.user.notifications)
  }

  unsavedTheme(): boolean {
    return this.theme !== this.user.theme
  }
}
</script>
