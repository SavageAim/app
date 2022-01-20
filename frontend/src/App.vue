<template>
  <div id="root" v-if="maintenance">
    <Nav :maintenance="maintenance" />
    <div class="hero is-fullheight-with-navbar">
      <div class="hero-body">
        <div class="container has-text-centered">
          <h1 class="title is-1">
            Savage <span class="has-text-danger">Aim</span> Maintenance
          </h1>
          <p class="subtitle">
            We're currently undergoing maintenance. We should be back soon!
          </p>
        </div>
      </div>
    </div>
  </div>
  <div id="root" v-else>
    <Nav />
    <div class="container is-fluid">
      <router-view></router-view>
    </div>
    <Footer v-if="($route.name || '').indexOf('errors') == -1" />
    <notifications position="bottom left" classes="notification" />
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import Changelog from './components/modals/changelog.vue'
import Footer from './components/footer.vue'
import Nav from './components/nav.vue'

@Component({
  components: {
    Footer,
    Nav,
  },
})
export default class App extends Vue {
  // Check the current version against the last version the user has seen, and if there's anything new, display the CHANGELOG modal
  checkChangelog(): void {
    const lastVersion = localStorage.lastVersion || ''
    const currVersion = this.$store.state.version
    if (lastVersion !== currVersion) {
      this.$modal.show(Changelog)

      localStorage.lastVersion = currVersion
    }
  }

  get maintenance(): boolean {
    if (process.env.VUE_APP_MAINTENANCE !== undefined) {
      return process.env.VUE_APP_MAINTENANCE === '1'
    }
    return false
  }

  async mounted(): Promise<void> {
    if (this.maintenance) return
    // Populate the store with static information for dropdowns later
    this.$store.dispatch('fetchGear')
    this.$store.dispatch('fetchItemLevels')
    this.$store.dispatch('fetchJobs')
    this.$store.dispatch('fetchTiers')

    // Check the changelog stuff
    this.checkChangelog()
  }
}
</script>

<style lang="scss">
@import './assets/base.scss';

.vue-notification-group {
  margin: 1rem;
}

#root {
  height: 100%;
}

#loading-text {
  justify-content: center;
}
</style>
