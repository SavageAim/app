<template>
  <div>
    <div class="breadcrumb">
      <ul>
        <li class="is-active"><a href="#">Create or Join a Team</a></li>
      </ul>
    </div>

    <div class="container">
      <router-link to="/team/new/" class="button is-fullwidth is-success icon-text">
        <span class="icon"><i class="material-icons">add</i></span>
        <span>Create New Team</span>
      </router-link>
      <div class="divider">OR</div>
      <div class="card">
        <div class="card-header">
          <div class="card-header-title">Join a Team</div>
        </div>
        <div class="card-content">
          <p>If you were given an invite code, insert it below and click Join to join a team!</p>
          <p>Alternatively, click the Create button above to make your own!</p>
          <hr />
          <div class="field">
          <label class="label" for="inviteCode">Invite Code</label>
            <div class="control">
              <input class="input" id="inviteCode" type="text" ref="inviteCode" :class="{'is-danger': joinError.length > 0}" />
            </div>
            <p class="help is-danger" v-if="joinError.length > 0">{{ joinError }}</p>
          </div>
          <button class="button is-success" @click="joinTeam">
            <span class="icon"><i class="material-icons">add</i></span>
            <span>Join</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component } from 'vue-property-decorator'
import SavageAimMixin from '@/mixins/savage_aim_mixin'

@Component
export default class TeamAdd extends SavageAimMixin {
  joinError = ''

  inviteCode(): string {
    return (this.$refs.inviteCode as HTMLInputElement).value
  }

  mounted(): void {
    document.title = 'Add Team - Savage Aim'
  }

  url(): string {
    return `/backend/api/team/join/${this.inviteCode()}/`
  }

  async joinTeam(): Promise<void> {
    // Check if the invite code is valid using the HEAD method
    this.joinError = ''

    try {
      const response = await fetch(this.url())
      if (response.ok) {
        // If the code is valid, redirect to the page
        this.$router.push(`/team/join/${this.inviteCode()}/`)
      }
      else {
        this.joinError = 'Invalid invite code! Please make sure you entered it correctly!'
      }
    }
    catch (e) {
      this.$notify({ text: `Error ${e} when fetching Team.`, type: 'is-danger' })
    }
  }
}
</script>

<style lang="scss">
</style>
