<template>
  <div class="column is-half-desktop">
    <div class="card">
      <div class="card-header">
        <div class="card-header-title">
          <span class="icon-text">
            <span class="icon is-hidden-touch" v-if="details.lead"><img src="/party_lead.png" alt="Team Lead" title="Team Lead" /></span>
            <span class="icon is-hidden-touch" v-else><img src="/party_member.png" alt="Team Member" title="Team Member" /></span>
            <span>{{ details.character.name }} @ {{ details.character.world }}</span>
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
            <img :src="`/job_icons/${details.bis_list.job.name}.png`" :alt="`${details.bis_list.job.name} job icon`" />
          </span>
        </div>
      </div>
      <div class="card-content">
        <BISTable :list="details.bis_list" :item-level="maxItemLevel" />
      </div>
      <footer class="card-footer">
        <a v-if="details.bis_list.external_link != null" target="_blank" :href="details.bis_list.external_link" class="card-footer-item">
          View on {{ details.bis_list.external_link.replace(/https?:\/\//, '').split('/')[0] }}
        </a>
        <template v-if="owner">
          <!-- Quick link to edit this bis list -->
          <router-link :to="`/characters/${details.character.id}/bis_list/${details.bis_list.id}/`" class="card-footer-item">
            Edit List
          </router-link>
          <!-- Link to update the TeamMember details with new character / bislist -->
          <router-link :to="`./member/${details.id}/`" class="card-footer-item">
            Change Character
          </router-link>
          <!-- Modal to confirm, leave team -->
          <!-- <a class="card-footer-item" v-if="!details.lead">
            Leave Team
          </a> -->
        </template>
        <!-- Admin Commands -->
        <!-- <template v-if="!owner && editable">
          Modal to confirm, kick from team
          <a class="card-footer-item">
            Kick from Team
          </a>
        </template> -->
      </footer>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator'
import BISTable from '@/components/bis_table.vue'
import Gear from '@/interfaces/gear'
import TeamMember from '@/interfaces/team_member'

@Component({
  components: {
    BISTable,
  },
})
export default class TeamMemberCard extends Vue {
  // Allows rendering other team member's cards with the kick button below
  @Prop()
  editable!: boolean

  @Prop()
  details!: TeamMember

  @Prop()
  maxItemLevel!: number

  // Flag stating whether the logged in user is the owner of the member on this card
  get owner(): boolean {
    return this.$store.state.user.id === this.details.character.user_id
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
</style>
