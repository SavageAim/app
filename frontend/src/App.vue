<template>
  <div id="root" v-shortkey.once="['ctrl', 'k']" @shortkey="openSwitcher">
    <Nav />
    <div class="container is-fluid">
      <router-view ref="viewComponent" :key="$route.fullPath"></router-view>
    </div>
    <Footer v-if="($route.name || '').indexOf('errors') == -1" />
    <notifications position="bottom left" classes="notification" />
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import Changelog from '@/components/modals/changelog.vue'
import Footer from '@/components/footer.vue'
import Nav from '@/components/nav.vue'
import SocketPayload from '@/interfaces/socket_payload'
import SavageAimMixin from '@/mixins/savage_aim_mixin'

@Component({
  components: {
    Footer,
    Nav,
  },
})
export default class App extends Vue {
  updateSocket!: WebSocket

  // Check that the backend server is up before loading the App properly
  async checkBackend(): Promise<void> {
    const response = await fetch('/backend/health/')
    if (response.ok) {
      this.loadData()
      Vue.nextTick(() => this.$forceUpdate)
      return
    }

    // If the request fails, it's almost guaranteed that the server is down, so ping a warning and set a check again in 30 seconds
    this.$notify({ text: 'Backend server could not be reached. There is probably an update being deployed. Checking again in 30 seconds.', type: 'is-warning' })
    setTimeout(this.checkBackend, 30 * 1000)
  }

  // Check the current version against the last version the user has seen, and if there's anything new, display the CHANGELOG modal
  checkChangelog(): void {
    const lastVersion = localStorage.lastVersion || ''
    const currVersion = this.$store.state.version
    if (lastVersion !== currVersion) {
      this.$modal.show(Changelog)

      localStorage.lastVersion = currVersion
    }
  }

  get viewComponent(): SavageAimMixin {
    return this.$refs.viewComponent as SavageAimMixin
  }

  async mounted(): Promise<void> {
    this.checkBackend()
  }

  loadData(): void {
    // Populate the store with static information for dropdowns later
    this.$store.dispatch('fetchUser')
    this.$store.dispatch('fetchGear')
    this.$store.dispatch('fetchItemLevels')
    this.$store.dispatch('fetchJobs')
    this.$store.dispatch('fetchTiers')

    // Check the changelog stuff
    this.checkChangelog()

    // Set up updates socket
    this.initSocket()
  }

  initSocket(): void {
    // Do all the set up and handling of the websocket
    const sock = new WebSocket(`${process.env.VUE_APP_WS_URL}/ws/updates/`)

    sock.onmessage = async (msg: MessageEvent) => {
      const payload = JSON.parse(msg.data) as SocketPayload

      switch (payload.model) {
      case 'bis':
        break
      case 'character':
        await this.$store.dispatch('fetchCharacters')
        break
      case 'loot':
        break
      case 'notification':
        await this.$store.dispatch('fetchNotifications')
        break
      case 'settings':
        await this.$store.dispatch('fetchUser')
        break
      case 'team':
        await this.$store.dispatch('fetchTeams')
        break
      default:
        Vue.notify({ text: `Unexpected packet model "${payload.model}" received.`, type: 'is-warning' })
      }
      payload.reloadUrls.forEach((url: string) => {
        if (this.$route.path.includes(url)) this.reloadView()
      })
    }

    this.updateSocket = sock
  }

  reloadView(): void {
    // Reload the view currently loaded in the router-view component
    this.viewComponent.load()
  }

  openSwitcher(): void {
    this.viewComponent.openSwitcher()
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
