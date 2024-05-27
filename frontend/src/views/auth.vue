<template>
  <div id="auth" class="container">
    <!-- Error Messages -->
    <div v-if="redirect" class="notification is-warning">
      <p>Please log in to continue.</p>
    </div>
    <div v-if="wasCancelled" class="notification is-info">
      Login attempt cancelled!
    </div>
    <div v-if="wasError" class="notification is-danger">
      An error occurred while attempting to log in. Please try again later or report it in the Discord server if it persists.
    </div>

    <!-- Actual Auth Stuff -->
    <div class="card">
      <div class="card-header">
        <div class="card-header-title">
          <h2 class="title">Login</h2>
        </div>
      </div>
      <div class="card-content">
        <div class="buttons is-centered">
          <a :href="buttonUrl" class="button is-blurple">
            <span class="icon is-24x24"><img id="discord-logo" src="/discord.svg" alt="Discord Logo" width="24" height="24" /></span>
            <span>Login with Discord</span>
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Watch } from 'vue-property-decorator'
import Dashboard from '@/components/dashboard.vue'
import Welcome from '@/components/welcome.vue'
import SavageAimMixin from '@/mixins/savage_aim_mixin'

@Component({
  components: {
    Dashboard,
    Welcome,
  },
})
export default class Auth extends SavageAimMixin {
  @Prop({ default: '' })
  next!: string

  @Prop({ default: false })
  redirect!: boolean

  get buttonUrl(): string {
    if (this.next === '') {
      return this.LOGIN_URL
    }
    return `${this.LOGIN_URL}?next=${this.next}`
  }

  @Watch('$store.state.user.id')
  checkAuth(): void {
    if (this.authenticated) {
      this.$router.push('/')
    }
  }

  mounted(): void {
    // If the user is authenticated, we don't need to be here
    this.checkAuth()
    document.title = 'Login - Savage Aim'
    console.log(this.buttonUrl)
  }

  // Handlers for the other potential error messages
  get wasCancelled(): boolean {
    return this.$route.query.auth_cancelled === '1'
  }

  get wasError(): boolean {
    return this.$route.query.auth_error === '1'
  }
}
</script>

<style lang="scss">
#discord-logo {
  height: 24px;
  width: 24px;
}
</style>
