<template>
  <div>
    <h2 class="title">
      Notifications
      <button class="button is-pulled-right is-success is-hidden-touch" @click="markAllAsRead" v-if="notifications.length > 0">Mark All As Read</button>
    </h2>
    <div v-if="loading">
      <button class="button is-static is-loading is-fullwidth">Loading</button>
    </div>

    <div v-else-if="notifications.length === 0">
      <h3 class="subtitle has-text-centered">No Notifications Found!</h3>
    </div>

    <div v-else>
      <button class="button is-success is-hidden-desktop is-fullwidth maar-button" @click="markAllAsRead">Mark All As Read</button>
      <NotificationCard v-for="notif in notifications" :notification="notif" :key="notif.id" />
    </div>
  </div>
</template>

<script lang="ts">
import * as Sentry from '@sentry/vue'
import { Component } from 'vue-property-decorator'
import NotificationCard from '@/components/notification_card.vue'
import Notification from '@/interfaces/notification'
import SavageAimMixin from '@/mixins/savage_aim_mixin'

@Component({
  components: {
    NotificationCard,
  },
})
export default class NotificationView extends SavageAimMixin {
  loading = true

  notifications: Notification[] = []

  created(): void {
    this.load()
    document.title = 'Notifications - Savage Aim'
  }

  async load(): Promise<void> {
    // Load the team data from the API
    try {
      const response = await fetch('/backend/api/notifications/')
      if (response.ok) {
        // Parse the JSON into a team and save it
        this.notifications = (await response.json()) as Notification[]
        this.loading = false
      }
      else {
        super.handleError(response.status)
      }
    }
    catch (e) {
      this.$notify({ text: `Error ${e} when fetching Notifications.`, type: 'is-danger' })
      Sentry.captureException(e)
    }
  }

  async markAllAsRead(): Promise<void> {
    try {
      const response = await fetch('/backend/api/notifications/', {
        method: 'POST',
        headers: {
          'X-CSRFToken': this.$cookies.get('csrftoken'),
        },
      })

      if (response.ok) {
        this.$store.dispatch('fetchNotifications')
        this.load()
      }
      else {
        super.handleError(response.status)
        this.$notify({ text: `Unexpected HTTP response ${response.status} received when marking notifications as read.`, type: 'is-danger' })
      }
    }
    catch (e) {
      this.$notify({ text: `Error ${e} when marking notifications as read.`, type: 'is-danger' })
      Sentry.captureException(e)
    }
  }
}
</script>

<style lang="scss">
.maar-button {
  margin-bottom: 1rem;
}
</style>
