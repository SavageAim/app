<template>
  <div id="auth" class="container">
    <div v-if="redirect" class="notification is-warning">
      <p>Please log in to continue.</p>
    </div>
    <div class="card">
      <div class="card-header">
        <div class="card-header-title">
          <h2 class="title">Login</h2>
        </div>
      </div>
      <div class="card-content">
        <div class="buttons is-centered">
          <a :href="LOGIN_URL" class="button is-blurple icon-text">
            <span class="icon"><img src="/discord.svg" alt="Discord Logo" /></span>
            <span>Login with Discord</span>
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop } from 'vue-property-decorator'
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
  @Prop({ default: false })
  redirect!: boolean

  mounted(): void {
    // If the user is authenticated, we don't need to be here
    if (this.authenticated) {
      this.$router.push('/')
    }
    document.title = 'Login - Savage Aim'
  }
}
</script>

<style lang="scss">

</style>
