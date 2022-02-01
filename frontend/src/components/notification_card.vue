<template>
  <a @clicl="open" class="box" :class="[notification.read ? 'read' : 'unread']">
    <article class="media">
      <figure class="media-left">
        <div class="icon has-text-primary">
          <i class="material-icons" v-if="notification.read">notifications</i>
          <i class="material-icons" v-else>notifications_active</i>
        </div>
      </figure>
      <div class="media-content">
        <p>{{ notification.text }}</p>
        <p>
          <small class="has-text-grey icon-text" data-microtip-position="right" role="tooltip" :aria-label="date">
            <span class="icon"><i class="material-icons">schedule</i></span>
            <span>{{ humanDate }}</span>
          </small>
        </p>
      </div>
    </article>
  </a>
</template>

<script lang="ts">
import dayjs from 'dayjs'
import relativeTime from 'dayjs/plugin/relativeTime'
import { Component, Prop, Vue } from 'vue-property-decorator'
import Notification from '@/interfaces/notification'

dayjs.extend(relativeTime)

@Component
export default class NotificationCard extends Vue {
  @Prop()
  notification!: Notification

  get date(): dayjs.Dayjs {
    return dayjs(this.notification.timestamp)
  }

  get humanDate(): string {
    return this.date.fromNow()
  }

  async markAsRead(): Promise<void> {
    try {
      const response = await fetch(`/backend/api/notifications/${this.notification.id}/`, {
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
        this.$notify({ text: `Unexpected HTTP response ${response.status} received when marking notification as read.`, type: 'is-danger' })
      }
    }
    catch (e) {
      this.$notify({ text: `Error ${e} when marking notification as read.`, type: 'is-danger' })
    }
  }

  open(): void {
    // Open a Notification, marking it as read in the process
    this.markAsRead(this.notification.id)

    // Open the link contained in the notification, using the router
    this.$router.push(this.notification.link)
    this.$emit('close')
  }
}
</script>

<style lang="scss">
</style>
