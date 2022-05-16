<template>
  <div class="column is-half-desktop">
    <div class="card">
      <div class="card-header">
        <div class="card-header-title">
          <span class="icon-text">
            <span class="icon is-hidden-touch" v-if="details.lead"><img src="/party_lead.png" alt="Team Lead" title="Team Lead" width="24" height="24" /></span>
            <span class="icon is-hidden-touch" v-else><img src="/party_member.png" alt="Team Member" title="Team Member" width="24" height="24" /></span>
            <span>{{ details.name }}</span>
          </span>
        </div>
        <div class="card-header-icon">
          <div class="tags has-addons is-hidden-touch">
            <span class="tag is-light">
              iL
            </span>
            <span class="tag" :class="[`is-${details.bis_list.job.role}`]">
              {{ details.bis_list.item_level }}
            </span>
          </div>
          <span class="icon">
            <img :src="`/job_icons/${details.bis_list.job.id}.png`" :alt="`${details.bis_list.job.name} job icon`" width="24" height="24" />
          </span>
        </div>
      </div>
      <div class="card-content">
        <BISTable :list="details.bis_list" :item-level="maxItemLevel" />
      </div>
      <footer class="card-footer" v-if="displayDropdown">
        <div class="dropdown is-centered card-footer-item" ref="dropdown">
          <div class="dropdown-trigger">
            <a class="icon-text" aria-haspopup="true" :aria-controls="`actions-${details.id}`" @click="toggleDropdown">
              <span>Actions</span>
              <span class="icon">
                <i class="material-icons" v-if="active">expand_less</i>
                <i class="material-icons" v-else>expand_more</i>
              </span>
            </a>
          </div>
          <div class="dropdown-menu" :id="`actions-${details.id}`" role="menu">
            <div class="dropdown-content">
              <a v-if="details.bis_list.external_link != null" target="_blank" :href="details.bis_list.external_link" class="card-footer-item">
                View on {{ details.bis_list.external_link.replace(/https?:\/\//, '').split('/')[0] }}
              </a>
              <template v-if="owner">
                <!-- Quick link to edit this bis list -->
                <hr class="dropdown-divider" />
                <router-link :to="`/characters/${details.character.id}/bis_list/${details.bis_list.id}/`" class="card-footer-item">
                  Edit List
                </router-link>
                <hr class="dropdown-divider" />
                <!-- Link to update the TeamMember details with new character / bislist -->
                <router-link :to="`./member/${details.id}/`" class="card-footer-item">
                  Change Character
                </router-link>
                <hr class="dropdown-divider" />
                <!-- Modal to confirm, leave team -->
                <a class="card-footer-item has-text-danger" @click="leave">
                  Leave Team
                </a>
              </template>
              <!-- Admin Commands -->
              <template v-if="!owner && editable">
                <!-- Modal to confirm, kick from team -->
                <hr class="dropdown-divider" />
                <a class="card-footer-item has-text-danger" @click="kick">Kick from Team</a>
              </template>
            </div>
          </div>
        </div>
      </footer>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator'
import BISTable from '@/components/bis_table.vue'
import KickFromTeam from '@/components/modals/confirmations/kick_from_team.vue'
import LeaveTeam from '@/components/modals/confirmations/leave_team.vue'
import TeamMember from '@/interfaces/team_member'

@Component({
  components: {
    BISTable,
  },
})
export default class TeamMemberCard extends Vue {
  active = false

  // Allows rendering other team member's cards with the kick button below
  @Prop()
  editable!: boolean

  @Prop()
  details!: TeamMember

  @Prop()
  maxItemLevel!: number

  @Prop()
  teamId!: number

  get displayDropdown(): boolean {
    // Check all the link cases in the dropdown and if none of them are true, we don't want to render the dropdown at all
    return (
      this.details.bis_list.external_link != null
      || this.owner
      || (!this.owner && this.editable)
    )
  }

  get dropdown(): HTMLElement {
    return this.$refs.dropdown as HTMLElement
  }

  kick(): void {
    this.$modal.show(KickFromTeam, { details: this.details, teamId: this.teamId }, { }, { closed: () => { this.$emit('reload') } })
  }

  leave(): void {
    this.$modal.show(LeaveTeam, { details: this.details, teamId: this.teamId })
  }

  // Flag stating whether the logged in user is the owner of the member on this card
  get owner(): boolean {
    return this.$store.state.user.id === this.details.character.user_id
  }

  toggleDropdown(): void {
    this.dropdown.classList.toggle('is-active')
    this.active = !this.active
  }
}
</script>

<style lang="scss">
.card-header-icon {
  cursor: default;
}

.card-header-icon > :not(:last-child) {
  margin-right: 0.5rem;
}

.card-header-icon .tags {
  margin-bottom: 0;

  & .tag {
    margin-bottom: 0;
  }
}

.dropdown-divider:first-child {
  display: none;
}

.dropdown.card-footer-item {
  padding: 0;

  & .dropdown-trigger {
    width: 100%;

    & a {
      width: calc(100% - 0.75rem);
      padding: 0.75rem;
      justify-content: center;
    }
  }
}
</style>
