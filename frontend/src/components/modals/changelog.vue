<template>
  <div>
    <div class="card-header">
      <div class="card-header-title">
        Changelog
      </div>
      <div class="card-header-icon">
        <a @click="() => { this.$emit('close') }" class="icon">
          <i class="material-icons">close</i>
        </a>
      </div>
    </div>
    <div class="card-content content">
      <h2 class="has-text-primary subtitle">{{ version }}</h2>
      <div class="divider"><i class="material-icons icon">expand_more</i> A Message <i class="material-icons icon">expand_more</i></div>
      <p>I had a little look at some DB metrics last night and I see a lot more people than I would have expected, since I've been slowly rolling the site out to friends' statics and such..</p>
      <p>Needless to say, I'm sorta overwhelmed with the use (in a good way, don't worry!)</p>
      <p>But, to those of you who have stumbled across my little website, I had no way of getting feedback from you so far...</p>
      <p>So there's a Discord server available now! It's smol and not very good but I figured it was important to get one out at least, and we can grow from there!</p>
      <p>Thank you to everyone who's been using the site so far, I will try my best to keep it going towards something ideal o7</p>
      <p class="has-text-centered">
        <a href="https://discord.gg/k8szJ5qAKw" class="button is-blurple icon-text" target="_blank">
          <span class="icon"><img src="/discord.svg" alt="Discord Logo" /></span>
          <span>Savage Aim Discord</span>
        </a>
      </p>
      <div class="divider"><i class="material-icons icon">expand_more</i> Major Changes <i class="material-icons icon">expand_more</i></div>
      <p>Notifications System has been added!</p>
      <p>
        The following events will give you notifications;
        <ul>
          <li>Character Verify requests failed or succeeded.</li>
          <li>Your Character has been put in charge of a Team it is in.</li>
          <li>Someone has joined a Team you lead.</li>
          <li>The Loot Tracker of a Team has updated one of your BIS Lists.</li>
        </ul>
      </p>
      <p>These are all toggleable, so you can disable any notification types you don't want to receive by visiting the Settings page!</p>
      <p>Currently the Notification system is polled every 30 seconds for updates, but I intend to make this truly live in the near future with instant updates when necessary!</p>

      <div class="divider"><i class="material-icons icon">expand_more</i> Minor Changes <i class="material-icons icon">expand_more</i></div>
      <p>Added Traffic Lights style colour scheme.</p>
      <p>Added more visibility into client side errors.</p>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'

@Component
export default class Changelog extends Vue {
  get version(): string {
    return this.$store.state.version
  }
}
</script>
