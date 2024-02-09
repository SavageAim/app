<template>
  <div class="column is-half-desktop">
    <div class="card">
      <div class="card-header">
        <div class="card-header-title">
          <span class="icon-text">
            <span class="icon is-hidden-touch" v-if="details.lead"><img src="/party_lead.png" alt="Team Lead" title="Team Lead" width="24" height="24" /></span>
            <span class="icon is-hidden-touch" v-else-if="details.character.proxy"><img src="/proxy.png" alt="Proxy Character" title="Proxy Character" width="24" height="24" /></span>
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
      <!-- Dropdown for mobile -->
      <footer class="card-footer is-hidden-desktop" v-if="displayFooter">
        <div class="dropdown is-centered card-footer-item" :class="{'is-active': active}">
          <div class="dropdown-trigger">
            <a class="icon-text" aria-haspopup="true" :aria-controls="`actions-${details.id}`" @click="toggleDropdown">
              <span class="icon"><i class="material-icons">more_vert</i></span>
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
                <span class="icon-text">
                  <span class="icon"><i class="material-icons">open_in_new</i></span>
                  <span>{{ details.bis_list.external_link.replace(/https?:\/\//, '').split('/')[0] }}</span>
                </span>
              </a>
              <template v-if="owner">
                <!-- Quick link to edit this bis list -->
                <hr class="dropdown-divider" />
                <router-link :to="`/characters/${details.character.id}/bis_list/${details.bis_list.id}/`" class="card-footer-item">
                  <span class="icon-text">
                    <span class="icon"><i class="material-icons">edit</i></span>
                    <span>Edit BIS</span>
                  </span>
                </router-link>
                <hr class="dropdown-divider" />
                <!-- Link to update the TeamMember details with new character / bislist -->
                <router-link :to="`./member/${details.id}/`" class="card-footer-item">
                  <span class="icon-text">
                    <span class="icon"><i class="material-icons">edit_note</i></span>
                    <span>Update Membership</span>
                  </span>
                </router-link>
                <hr class="dropdown-divider" />
                <!-- Modal to confirm, leave team -->
                <a class="card-footer-item has-text-danger" @click="leave">
                  <span class="icon-text">
                    <span class="icon"><i class="material-icons">not_interested</i></span>
                    <span>Leave Team</span>
                  </span>
                </a>
              </template>
            </div>
          </div>
        </div>
      </footer>

      <!-- No Dropdown for Desktop -->
      <footer class="card-footer has-text-link is-hidden-touch" v-if="displayFooter">
        <a target="_blank" :href="details.bis_list.external_link" class="card-footer-item" v-if="details.bis_list.external_link != null">
          <span class="icon-text">
            <span class="icon"><i class="material-icons">open_in_new</i></span>
            <span>{{ details.bis_list.external_link.replace(/https?:\/\//, '').split('/')[0] }}</span>
          </span>
        </a>

        <template v-if="owner">
          <!-- Quick link to edit this bis list -->
          <router-link :to="`/characters/${details.character.id}/bis_list/${details.bis_list.id}/`" class="card-footer-item">
            <span class="icon-text">
              <span class="icon"><i class="material-icons">edit</i></span>
              <span>Edit BIS</span>
            </span>
          </router-link>
          <!-- Link to update the TeamMember details with new character / bislist -->
          <router-link :to="`./member/${details.id}/`" class="card-footer-item">
            <span class="icon-text">
              <span class="icon"><i class="material-icons">edit_note</i></span>
              <span>Update Membership</span>
            </span>
          </router-link>
          <!-- Modal to confirm, leave team -->
          <a class="card-footer-item has-text-danger" @click="leave">
            <span class="icon-text">
              <span class="icon"><i class="material-icons">not_interested</i></span>
              <span>Leave Team</span>
            </span>
          </a>
        </template>
      </footer>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator'
import BISTable from '@/components/bis_table.vue'
import LeaveTeam from '@/components/modals/confirmations/leave_team.vue'
import TeamMember from '@/interfaces/team_member'

@Component({
  components: {
    BISTable,
  },
})
export default class TeamMemberCard extends Vue {
  active = false

  @Prop()
  details!: TeamMember

  @Prop()
  maxItemLevel!: number

  @Prop()
  teamId!: number

  get displayFooter(): boolean {
    // Check all the link cases in the footer and if none of them are true, we don't want to render the card footer at all
    return (
      this.details.bis_list.external_link != null
      || this.owner
    )
  }

  leave(): void {
    this.$modal.show(LeaveTeam, { details: this.details, teamId: this.teamId })
  }

  // Flag stating whether the logged in user is the owner of the member on this card
  get owner(): boolean {
    return this.$store.state.user.id === this.details.character.user_id
  }

  toggleDropdown(): void {
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
