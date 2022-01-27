<template>
  <nav class="navbar is-fixed-top" role="navigation" aria-label="main navigation">
    <div class="navbar-brand">
      <router-link to="/" class="navbar-item">
        <h2 class="title">Savage <span class="has-text-danger">Aim</span></h2>
      </router-link>

      <a role="button" class="navbar-burger" aria-label="menu" aria-expanded="false" ref="burger" @click="toggleNavbar">
        <span aria-hidden="true">
          <div class="badge is-info" v-if="hasUnreads">1</div>
        </span>
        <span aria-hidden="true"></span>
        <span aria-hidden="true"></span>
      </a>
    </div>

    <div ref="navbar" class="navbar-menu" v-if="!maintenance">
      <div class="navbar-start">
        <router-link to="/" class="navbar-item">
          <div class="icon-text">
            <span class="icon">
              <i class="material-icons">home</i>
            </span>
            <span>Home</span>
          </div>
        </router-link>
      </div>

      <div class="navbar-end">
        <a href="#" @click="showLegend" class="navbar-item">
          <div class="icon-text">
            <span class="icon"><i class="material-icons">bar_chart</i></span>
            <span>Colours Explanation</span>
          </div>
        </a>

        <template v-if="authenticated">
          <a href="#" class="navbar-item notifications">
            <div class="icon-text" v-if="hasUnreads">
              <span class="icon">
                <span class="badge is-info">1</span>
                <i class="material-icons">notifications_active</i>
              </span>
              <span class="is-hidden-desktop">Notifications</span>
            </div>
            <div class="icon-text" v-else>
              <span class="icon">
                <i class="material-icons">notifications</i>
              </span>
              <span class="is-hidden-desktop">Notifications</span>
            </div>
          </a>

          <div class="navbar-item has-dropdown is-hoverable">
            <div class="navbar-link" id="user-item">
              <figure class="image user-image" v-if="user.avatar_url">
                <img class="is-rounded" id="profile-img" :src="user.avatar_url" alt="Discord Profile Image" />
              </figure>
              <span>{{ user.username }}</span>
            </div>

            <div class="navbar-dropdown">
              <router-link class="navbar-item" to="/settings/">
                <div class="icon-text">
                  <span class="icon is-hidden-desktop"><i class="material-icons">settings</i></span>
                  <span>Settings</span>
                </div>
              </router-link>
              <a class="navbar-item" @click="logout">
                <div class="icon-text">
                  <span class="icon is-hidden-desktop"><i class="material-icons">logout</i></span>
                  <span>Logout</span>
                </div>
              </a>
            </div>
          </div>
        </template>
        <template v-else>
          <router-link class="navbar-item" to="/auth/">
            <div class="icon-text">
              <span class="icon"><i class="material-icons">key</i></span>
              <span>Login</span>
            </div>
          </router-link>
        </template>
      </div>
    </div>
  </nav>
</template>

<script lang="ts">
import { Component, Prop, Watch } from 'vue-property-decorator'
import Legend from './modals/legend.vue'
import SavageAimMixin from '@/mixins/savage_aim_mixin'

@Component
export default class Nav extends SavageAimMixin {
  @Prop({ default: false })
  maintenance!: boolean

  // Display the notifications flag
  hasUnreads = false

  // Only check for the refs after we've been mounted
  isMounted = false

  get burger(): Element {
    return this.$refs.burger as Element
  }

  get nav(): Element {
    return this.$refs.navbar as Element
  }

  destroyed(): void {
    this.isMounted = false
  }

  toggleNavbar(): void {
    this.burger.classList.toggle('is-active')
    this.nav.classList.toggle('is-active')
  }

  beforeCreate(): void {
    // Tell the store to attempt to fetch the logged in user
    this.$store.dispatch('fetchUser')
  }

  async logout(): Promise<void> {
    // Send a GET request to the logout url, and that should be all we need to do
    await fetch(this.LOGOUT_URL)
    this.$store.commit('resetUser')
    this.$router.push('/')
    this.$notify({ text: 'Successfully logged out!', type: 'is-success' })
  }

  mounted(): void {
    this.isMounted = true
  }

  // Display the colour legend chart modal
  showLegend(): void {
    this.$modal.show(Legend)
  }

  // Watch the location.path value and any time it changes run the function
  @Watch('$route', { immediate: true, deep: true })
  urlChange(): void {
    if (this.isMounted) {
      this.burger.classList.remove('is-active')
      this.nav.classList.remove('is-active')
    }
  }
}
</script>

<style lang="scss">
@import '../assets/variables.scss';

nav {
  border-bottom: 1px solid $shade-dark;
}

.navbar-brand .title {
  font-weight: 300;
}

.navbar-burger {
  &:hover {
    color: $accent-blue;
  }
}

.user-image {
  width: 40px;
  height: 40px;
  margin-right: 0.5rem;
}

#profile-img {
  max-height: 40px;
}

#user-item {
  display: flex;
  align-items: center;
}

.badge {
  z-index: 10;
}

.navbar-burger.is-active .badge {
  display: none;
}

.notifications .badge {
  top: unset;
  right: unset;
}
</style>
