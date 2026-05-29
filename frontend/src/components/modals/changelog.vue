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
      <div class="divider"><i class="material-icons icon">expand_more</i> We're Back! <i class="material-icons icon">expand_more</i></div>
      <p>If you can see this, then we're back online!</p>
      <p>We've successfully moved host to a new provider that hopefully won't go away any time soon, and we should be better than ever on an infrastructure angle!</p>
      <p>Some friends and I have done some initial testing to make sure all is as it should be, but if there are any issues at all I'll be happy to fix them asap!</p>
      <p>Also, if you would like to help cover the costs, there's a <b>COMPLETELY OPTIONAL</b> Patreon link in the footer of the page.</p>
      <p>There's no real benefits I can offer to Patreon supporters as I want the site to remain ad-free for everyone but I am always open to suggestions!</p>

      <div class="divider"><i class="material-icons icon">expand_more</i> Except <i class="material-icons icon">expand_more</i></div>
      <p><b>TL;DR: Websockets have been disabled for now, so real time updates from team members etc won't be happening.</b></p>
      <p>Originally, we had just a couple of VMs that hosted the website since I was given them for free.</p>
      <p>I've migrated to a scaling-on-demand system in order to keep pricing down when the site is not in use.</p>
      <p>However, we would still need something like Redis in order to facilitate the websocket system.</p>
      <p>Hosting one of those is insanely pricey for something that is, in effect, a hobby project.</p>
      <p>If things change in the future, I really hope to put out an update saying Websockets / Real Time Updates are back.</p>
      <p>But for now, I think it's an understandable thing to cut while trying to get things back up and running.</p>
      <p>I'm really sorry if this is an inconvenience to you.</p>
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

<style lang="scss">
</style>
