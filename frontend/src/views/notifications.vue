<template>
  <div>
    <h2 class="title">
      Notifications
      <button class="button is-pulled-right is-success" v-if="notifications.length > 0">Mark All As Read</button>
    </h2>
    <div v-if="loading">
      <button class="button is-static is-loading is-fullwidth">Loading</button>
    </div>

    <div v-else-if="notifications.length === 0">
      <h3 class="subtitle has-text-centered">No Notifications Found!</h3>
    </div>

    <template v-else>
      <NotificationCard v-for="notif in notifications" :notification="notif" :key="notif.id" />
    </template>
  </div>
</template>

<script lang="ts">
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
    this.fetchData()
    document.title = 'Notifications - Savage Aim'
  }

  async fetchData(): Promise<void> {
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
      }
      else {
        super.handleError(response.status)
        this.$notify({ text: `Unexpected HTTP response ${response.status} received when marking notifications as read.`, type: 'is-danger' })
      }
    }
    catch (e) {
      this.$notify({ text: `Error ${e} when marking notifications as read.`, type: 'is-danger' })
    }
  }
}
</script>

<style lang="scss">
</style>
