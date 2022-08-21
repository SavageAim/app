<template>
  <div class="box proxy-box">
    <div class="proxy-member-name">
      {{ member.name }}
    </div>
    <div class="desktop-buttons is-hidden-touch">
      <div class="buttons is-grouped" v-if="userHasPermission">
        <router-link :to="`../proxies/${member.character.id}/`" class="button is-primary is-outlined">
          Edit Proxy BIS
        </router-link>
        <button class="button is-danger is-outlined" @click="kick">
          <span>Kick From Team</span>
        </button>
      </div>
    </div>
    <div class="touch-buttons is-hidden-desktop">
      <div class="buttons" v-if="userHasPermission">
        <router-link :to="`../proxies/${member.character.id}/`" class="button is-primary is-outlined is-fullwidth">
          Edit Proxy BIS
        </router-link>
        <button class="button is-danger is-outlined is-fullwidth" @click="kick">
          <span>Kick From Team</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'
import KickFromTeam from '@/components/modals/confirmations/kick_from_team.vue'
import TeamMember from '@/interfaces/team_member'

@Component
export default class ProxyMemberManager extends Vue {
  @Prop()
  member!: TeamMember

  @Prop()
  teamId!: string

  @Prop()
  userHasPermission!: boolean

  kick(): void {
    this.$modal.show(KickFromTeam, { details: this.member, teamId: this.teamId }, { }, { closed: () => { this.$emit('reload') } })
  }
}
</script>

<style lang="scss" scoped>
.proxy-member-name {
  display: inline-block;
}

.desktop-buttons {
  display: inline-block;
}

.touch-buttons {
  margin-top: 1rem;
}

@media screen and (min-width: 1024px) {
  .proxy-box {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
}
</style>
