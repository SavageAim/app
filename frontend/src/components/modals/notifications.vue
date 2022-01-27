<template>
  <div>
    <div class="card-header">
      <div class="card-header-title">
        Notifications
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
        <button class="button is-success is-fullwidth">Mark all as read</button>
      </div>

      <a :href="`#${notif.target}`" class="box" v-for="notif in notifications" :class="[notif.read ? 'read' : 'unread']" :key="notif.id">
        <article class="media">
          <figure class="media-left">
            <div class="icon has-text-primary">
              <i class="material-icons" v-if="notif.read">notifications</i>
              <i class="material-icons" v-else>notifications_active</i>
            </div>
          </figure>
          <div class="media-content">
            <p><span class="has-text-info">{{ notif.actor }}</span> {{ notif.verb }} <span class="has-text-info" v-if="notif.action_object !== null">{{ notif.action_object }}</span></p>
            <p><small class="has-text-grey">{{ notif.date }}</small></p>
          </div>
        </article>
      </a>

      <div class="pagination is-centered" id="notif-pager" role="navigation" aria-label="pagination">
        <a class="pagination-previous" v-if="page > 1">Previous Page</a>
        <a class="pagination-previous is-disabled">Previous Page</a>
        <ul class="pagination-list">
          <li class="pagination-ellipsis">Page {{ page }} of {{ maxPages }}</li>
        </ul>
        <a class="pagination-next" v-if="page < maxPages">Next Page</a>
        <a class="pagination-next is-disabled" v-else>Next Page</a>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'

@Component
export default class Notifications extends Vue {
  notifications = [
    {
      id: 2,
      read: false,
      actor: 'Erika Yukiko @ Shiva (Light)',
      verb: 'has joined',
      action_object: 'Hi Wiki!',
      date: '1d ago',
      target: '/team/fb2e8fdf-afed-4799-bc28-ac093b9b8a79/',
    },
    {
      id: 1,
      read: true,
      actor: 'Erika Yukiko @ Lich (Light)',
      verb: 'has been verified!',
      action_object: null,
      date: '2d ago',
      target: '/characters/1/',
    },
  ]

  notifsPerPage = 5

  page = 1

  get maxPages(): number {
    return Math.ceil(this.notifications.length / this.notifsPerPage)
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
