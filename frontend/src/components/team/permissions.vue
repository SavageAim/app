<template>
  <div class="container">
    <div class="card">
      <div class="card-header">
        <div class="card-header-title">
          Member Permissions
        </div>
      </div>
      <div class="card-content">
        <!-- Desktop -->
        <table class="table is-fullwidth is-bordered is-hidden-touch">
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
              <td class="has-text-centered">
                <PermissionInput label="Loot Manager Control" :display-label="false" :enabled="editable" v-model="member.permissions.loot_manager" />
              </td>
              <td class="has-text-centered">
                <PermissionInput label="Team Character Management" :display-label="false" :enabled="editable" v-model="member.permissions.team_characters" />
              </td>
            </tr>
          </tbody>
        </table>

        <!-- Mobile -->
        <ul class="mobile-list is-hidden-desktop">
          <li v-for="member in team.members" :key="member.id">
            <h3 class="subtitle">
              {{ member.name }}
            </h3>
            <PermissionInput label="Loot Manager Control" :enabled="editable" v-model="member.permissions.loot_manager" />
            <PermissionInput label="Team Character Management" :enabled="editable" v-model="member.permissions.team_characters" />
          </li>
        </ul>
      </div>
      <div class="card-footer">
        <a class="has-text-success card-footer-item" @click="save">Save</a>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop } from 'vue-property-decorator'
import PermissionInput from '@/components/team/permission_input.vue'
import Team from '@/interfaces/team'
import SavageAimMixin from '@/mixins/savage_aim_mixin'

@Component({
  components: {
    PermissionInput,
  },
})
export default class TeamPermissions extends SavageAimMixin {
  @Prop()
  editable!: boolean

  @Prop()
  team!: Team

  get url(): string {
    return `/backend/api/team/${this.$route.params.id}/`
  }

  save(): void {
    console.log(this.team.members)
  }
}
</script>

<style lang="scss">
.mobile-list {
  & li {
    & label {
      margin-left: 2rem;
    }

    &:not(:last-child) {
      padding-bottom: 1rem;
      margin-bottom: 1rem;
      border-bottom: 1px solid;
    }

    & .subtitle {
      margin-bottom: 0.75rem;
    }
  }
}
</style>
