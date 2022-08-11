<template>
  <div class="box">
    <div class="level">
      <div class="level-left">
        <div class="level-item">
          <div class="content">{{ member.name }}</div>
        </div>
      </div>
      <div class="level-right">
        <div class="level-item">
          <div class="buttons is-grouped" v-if="userHasPermission">
            <router-link :to="`../proxies/${member.character.id}/`" class="button is-primary is-outlined">
              Edit Proxy BIS
            </router-link>
            <button class="button is-danger is-outlined" @click="kick">
              <span>Kick From Team</span>
            </button>
          </div>
        </div>
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
  userHasPermission!: boolean

  kick(): void {
    this.$modal.show(KickFromTeam, { details: this.member, teamId: this.$route.params.id }, { }, { closed: () => { console.log(this); this.$emit('reload') } })
  }
}
</script>

<style lang="scss">

</style>
