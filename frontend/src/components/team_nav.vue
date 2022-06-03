<template>
  <div class="field has-addons">
    <p class="control">
      <router-link :to="mainUrl" class="button is-link" :class="{ 'is-outlined': !isActive(mainUrl) }">
        <div class="icon-text is-hidden-touch">
          <span class="icon is-small">
            <i class="material-icons">group</i>
          </span>
          <span>Team Details</span>
        </div>
        <span class="icon is-small is-hidden-desktop">
          <i class="material-icons">group</i>
        </span>
      </router-link>
    </p>
    <p class="control">
      <router-link :to="lootUrl" class="button is-link" :class="{ 'is-outlined': !isActive(lootUrl) }">
        <div class="icon-text is-hidden-touch">
          <span class="icon is-small">
            <i class="material-icons">receipt_long</i>
          </span>
          <span>Loot Manager</span>
        </div>
        <span class="icon is-small is-hidden-desktop">
          <i class="material-icons">receipt_long</i>
        </span>
      </router-link>
    </p>
    <p class="control">
      <router-link :to="managementUrl" class="button is-link" :class="{ 'is-outlined': !isActive(managementUrl) }">
        <div class="icon-text is-hidden-touch">
          <span class="icon is-small">
            <i class="material-icons">manage_accounts</i>
          </span>
          <span>Management</span>
        </div>
        <span class="icon is-small is-hidden-desktop">
          <i class="material-icons">manage_accounts</i>
        </span>
      </router-link>
    </p>
    <p class="control" v-if="editable">
      <router-link :to="settingsUrl" class="button is-link" :class="{ 'is-outlined': !isActive(settingsUrl) }">
        <div class="icon-text is-hidden-touch">
          <span class="icon is-small">
            <i class="material-icons">settings</i>
          </span>
          <span>Settings</span>
        </div>
        <span class="icon is-small is-hidden-desktop">
          <i class="material-icons">settings</i>
        </span>
      </router-link>
    </p>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'

@Component
export default class TeamNav extends Vue {
  @Prop()
  editable!: boolean

  get mainUrl(): string {
    return `/team/${this.$route.params.id}/`
  }

  get managementUrl(): string {
    return `/team/${this.$route.params.id}/management/`
  }

  get lootUrl(): string {
    return `/team/${this.$route.params.id}/loot/`
  }

  get settingsUrl(): string {
    return `/team/${this.$route.params.id}/settings/`
  }

  isActive(path: string): boolean {
    // Return a flag indicating whether the supplied url is the current one
    return this.$route.path === path
  }
}
</script>

<style lang="scss" scoped>
.icon.is-hidden-desktop {
  margin: 0!important;
}
</style>
