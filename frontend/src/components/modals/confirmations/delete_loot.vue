<template>
  <div>
    <div class="card-header">
      <div class="card-header-title">{{ team.name }} - Loot History Deletion</div>
      <div class="card-header-icon">
        <a @click="() => { this.$emit('close') }" class="icon">
          <i class="material-icons">close</i>
        </a>
      </div>
    </div>
    <div class="card-content">
      <h2 class="subtitle">Are you sure you want to delete these Loot History entries?</h2>
      <hr />
      <ul>
        <li v-for="history in items" :key="history.id">
          <b>Item: </b> {{ history.item }}<br />
          <b>Obtained By: </b> {{ history.member }}<br />
          <b>On: </b> {{ history.obtained }}<br />
          <b>Via: </b>
          <span class="has-text-info" v-if="history.greed">Greed</span>
          <span class="has-text-primary" v-else>Need</span>
        </li>
      </ul>
    </div>
    <div class="card-footer">
      <a class="card-footer-item has-text-danger" @click="deleteLoot">
        <span class="icon-text">
          <span class="icon"><i class="material-icons">delete</i></span>
          <span>Delete</span>
        </span>
      </a>
      <a class="card-footer-item has-text-link" @click="() => { this.$emit('close') }">
        <span class="icon-text">
          <span class="icon"><i class="material-icons">close</i></span>
          <span>Cancel</span>
        </span>
      </a>
    </div>
  </div>
</template>

<script lang="ts">
import * as Sentry from '@sentry/vue'
import { Component, Prop, Vue } from 'vue-property-decorator'
import { Loot } from '@/interfaces/loot'
import Team from '@/interfaces/team'

@Component
export default class DeleteLoot extends Vue {
  @Prop()
  items!: Loot[]

  @Prop()
  team!: Team

  get url(): string {
    return `/backend/api/team/${this.team.id}/loot/`
  }

  async deleteLoot(): Promise<void> {
    const body = JSON.stringify({ items: this.items.map((item: Loot) => item.id) })
    try {
      const response = await fetch(this.url, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': Vue.$cookies.get('csrftoken'),
        },
        body,
      })

      if (response.ok) {
        // Attempt to parse the json, get the id, and then redirect
        this.$emit('close')
        this.$notify({ text: 'Loot History entries deleted successfully!', type: 'is-success' })
      }
      else {
        this.$notify({ text: `Unexpected response ${response.status} when attempting to delete Loot History.`, type: 'is-danger' })
      }
    }
    catch (e) {
      this.$notify({ text: `Error ${e} when attempting to delete Loot History.`, type: 'is-danger' })
      Sentry.captureException(e)
    }
  }
}
</script>

<style lang="scss" scoped>
li:not(:last-child) {
  margin-bottom: 0.75rem;
  padding-bottom: 0.75rem;
  border-bottom: 2px solid #17181c;
}
</style>
