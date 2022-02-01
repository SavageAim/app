<template>
  <div>
    <div class="card-header">
      <div class="card-header-title">
        Latest 20 Notifications
      </div>
      <div class="card-header-icon">
        <a class="icon" @click="() => { this.$emit('close') }">
          <i class="material-icons">close</i>
        </a>
      </div>
    </div>
    <div class="card-content">
      <div class="content">
        <p>Click or tap notifications to open them, or click the button below to mark all as read.</p>
        <div class="field has-addons" >
          <div class="control is-expanded">
            <button class="button is-success is-fullwidth" @click="markAllAsRead">
              <span>Mark All As Read</span>
            </button>
          </div>
          <div class="control is-expanded">
            <button @click="viewAll" class="button is-info is-fullwidth">
              <span>View All Notifications</span>
            </button>
          </div>
        </div>
      </div>

      <template v-if="notifications.length > 0">
        <a @click="() => open(i)" class="box" v-for="i in pageRange()" :class="[notifications[i].read ? 'read' : 'unread']" :key="notifications[i].id">
          <article class="media">
            <figure class="media-left">
              <div class="icon has-text-primary">
                <i class="material-icons" v-if="notifications[i].read">notifications</i>
                <i class="material-icons" v-else>notifications_active</i>
              </div>
            </figure>
            <div class="media-content">
              <p>{{ notifications[i].text }}</p>
              <p>
                <small class="has-text-grey icon-text" data-microtip-position="right" role="tooltip" :aria-label="getTimestamp(i)">
                  <span class="icon"><i class="material-icons">schedule</i></span>
                  <span>{{ getHumanDisplay(i) }}</span>
                </small>
              </p>
            </div>
          </article>
        </a>

        <div class="pagination is-centered" id="notif-pager" role="navigation" aria-label="pagination">
          <a class="pagination-previous" @click="page--" v-if="page > 1">Previous Page</a>
          <a class="pagination-previous is-disabled" v-else>Previous Page</a>
          <ul class="pagination-list">
            <li class="pagination-ellipsis">Page {{ page }} of {{ maxPages }}</li>
          </ul>
          <a class="pagination-next" @click="page++" v-if="page < maxPages">Next Page</a>
          <a class="pagination-next is-disabled" v-else>Next Page</a>
        </div>
      </template>
      <p v-else class="has-text-info has-text-centered">No Notifications have been received!</p>
    </div>
  </div>
</template>

<script lang="ts">
import dayjs from 'dayjs'
import relativeTime from 'dayjs/plugin/relativeTime'
import { Component, Vue } from 'vue-property-decorator'
import Notification from '@/interfaces/notification'

dayjs.extend(relativeTime)

@Component
export default class Notifications extends Vue {
  notifsPerPage = 4

  page = 1

  getHumanDisplay(index: number): string {
    return dayjs(this.notifications[index].timestamp).fromNow()
  }

  getTimestamp(index: number): dayjs.Dayjs {
    return dayjs(this.notifications[index].timestamp)
  }

  get maxPages(): number {
    return Math.ceil(this.notifications.length / this.notifsPerPage)
  }

  get notifications(): Notification[] {
    return this.$store.state.notifications
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

  async markSingleAsRead(id: number): Promise<void> {
    try {
      const response = await fetch(`/backend/api/notifications/${id}/`, {
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

  open(index: number): void {
    // Open a Notification, marking it as read in the process
    const notif = this.notifications[index]
    this.markSingleAsRead(notif.id)

    // Open the link contained in the notification, using the router
    this.$router.push(notif.link)
    this.$emit('close')
  }

  pageRange(): ReadonlyArray<number> {
    const size = this.page * this.notifsPerPage < this.notifications.length ? this.notifsPerPage : this.notifications.length % this.notifsPerPage
    const start = (this.page - 1) * this.notifsPerPage
    return Array.from({ length: size }, (x, i) => i + start)
  }

  viewAll(): void {
    this.$router.push('/notifications/')
    this.$emit('close')
  }
}
</script>

<style lang="scss">
@import '../../assets/variables.scss';

a.box.unread {
  border: 1px solid $main-colour;

  &:hover {
    box-shadow: 0 0.5em 1em -0.125em rgba(237, 237, 232, 0.1);
  }
}

a.box.read {
  &:hover {
    color: unset;
    box-shadow: 0 0.5em 1em -0.125em rgba(237, 237, 232, 0.1), 0 0 0 1px rgba(237, 237, 232, 0.1);
  }
}

#notif-pager {
  & .pagination-previous, & .pagination-next {
    width: 25%;

    &.is-disabled {
      visibility: hidden;
    }
  }
}
</style>
