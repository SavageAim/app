<template>
  <div>
    <div class="card-header">
      <div class="card-header-title">Edit Permissions for {{ member.name }}</div>
      <div class="card-header-icon">
        <a class="icon" @click="() => { this.$emit('close') }">
          <i class="material-icons">close</i>
        </a>
      </div>
    </div>
    <div class="card-content">
      <label class="checkbox" for="loot-manager">
        <input type="checkbox" id="loot-manager" value="1" :checked="member.permissions.loot_manager">
        Loot Manager - Hand out Loot via Loot Manager
      </label>
      <br />
      <label class="checkbox" for="proxy-manager">
        <input type="checkbox" id="proxy-manager" value="2" :checked="member.permissions.proxy_manager">
        Proxy Manager - Manage Proxy Characters
      </label>
    </div>
    <footer class="card-footer">
      <a class="card-footer-item has-text-success" @click="save">
        <span class="icon-text">
          <span class="icon"><i class="material-icons">save</i></span>
          <span>Save</span>
        </span>
      </a>
      <a class="card-footer-item has-text-link" @click="() => { this.$emit('close') }">
        <span class="icon-text">
          <span class="icon"><i class="material-icons">close</i></span>
          <span>Cancel</span>
        </span>
      </a>
    </footer>
  </div>
</template>

<script lang="ts">
import * as Sentry from '@sentry/vue'
import { Component, Prop, Vue } from 'vue-property-decorator'
import TeamMember from '@/interfaces/team_member'

@Component
export default class Permissions extends Vue {
  @Prop()
  member!: TeamMember

  @Prop()
  teamId!: number

  get url(): string {
    return `/backend/api/team/${this.teamId}/member/${this.member.id}/permissions/`
  }

  async save(): Promise<void> {
    const checkboxes = this.$el.querySelectorAll('input[type="checkbox"]')
    let permissions = 0
    checkboxes.forEach((el: Element) => {
      const input = el as HTMLInputElement
      if (input.checked) permissions += parseInt(input.value, 10)
    })

    // Send a request to update the permissions of the specified user
    try {
      const response = await fetch(this.url, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': Vue.$cookies.get('csrftoken'),
        },
        body: JSON.stringify({ permissions }),
      })

      if (response.ok) {
        // Empty response so we can just reload the page
        this.$notify({ text: 'Permissions successfully updated!', type: 'is-success' })
        this.$emit('close')
      }
      else {
        this.$notify({ text: `Unexpected response ${response.status} when attempting to update Permissions.`, type: 'is-danger' })
      }
    }
    catch (e) {
      this.$notify({ text: `Error ${e} when attempting to update Permissions.`, type: 'is-danger' })
      Sentry.captureException(e)
    }
  }
}
</script>

<style lang="scss">
label:not(:last-child) {
  margin-bottom: 1rem;
}
</style>
