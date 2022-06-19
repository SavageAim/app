<template>
  <div class="container">
    <div class="card">
      <div class="card-header">
        <div class="card-header-title">
          Member Permissions
        </div>
      </div>
      <div class="card-content">
        <table class="table is-fullwidth is-bordered">
          <thead>
            <tr>
              <th></th>
              <th class="has-text-centered">Loot Manager Control</th>
              <th class="has-text-centered">Team Character Management</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="member in team.members" :key="member.id">
              <th>{{ member.name }}</th>
              <td class="has-text-centered"><input type="checkbox" /></td>
              <td class="has-text-centered"><input type="checkbox" /></td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="card-footer">
        <a class="has-text-success card-footer-item">Save</a>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop } from 'vue-property-decorator'
import { TeamUpdateErrors } from '@/interfaces/responses'
import Team from '@/interfaces/team'
import TeamMember from '@/interfaces/team_member'
import SavageAimMixin from '@/mixins/savage_aim_mixin'

@Component
export default class TeamPermissions extends SavageAimMixin {
  @Prop()
  team!: Team

  get url(): string {
    return `/backend/api/team/${this.$route.params.id}/`
  }
}
</script>

<style lang="scss">
</style>
