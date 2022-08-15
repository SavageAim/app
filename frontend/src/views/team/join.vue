<template>
  <div>
    <div v-if="!teamLoaded">
      <button class="button is-static is-loading is-fullwidth">Loading</button>
    </div>

    <template v-else>
      <div class="breadcrumb">
        <ul>
          <li><router-link to="/team/">Create or Join a Team</router-link></li>
          <li class="is-active"><a>Join a Team</a></li>
        </ul>
      </div>

      <div class="container">
        <!-- Team display box here -->
        <div class="card">
          <div class="card-header">
            <div class="card-header-title">You have been invited to join;</div>
          </div>
          <div class="card-content">
            <div class="box">
              <TeamBio :team="team" :displayIcons="false" />
            </div>
          </div>
        </div>

        <div class="columns">
          <div class="column">
            <div class="card">
              <div class="card-header">
                <div class="card-header-title">Select a Character and BIS List</div>
              </div>
              <div class="card-content" v-if="characters.length">
                <TeamMemberForm ref="form" :bis-list-id-errors="errors.bis_list_id" :character-id-errors="errors.character_id" />
                <button class="button is-success" @click="join">Join!</button>
              </div>
              <div class="card-content content" v-else>
                <p>
                  Your account currently has no Characters. You have two choices as to how you proceed;
                  <ol>
                    <li>
                      If a Character you own is listed in the Claim a Proxy card <span class="is-hidden-desktop">below</span><span class="is-hidden-touch">to the right</span>, you may click on them to attempt to claim them.
                      <br />
                      When verified, you will have automatically joined the Team and will not need to visit this page again.
                    </li>
                    <li>
                      If your Character isn't present as a Proxy, you may click the button below to open the Add Character page in a new tab.
                      <br />
                      When added and verified, return to this tab and this page should have instantly updated to display a dropdown with your new Character in it.
                    </li>
                  </ol>
                </p>
                <a href="/characters/new/" target="_blank" class="button is-success is-fullwidth">
                  <span class="icon-text">
                    <span class="icon"><i class="material-icons">open_in_new</i></span>
                    <span>Add Character</span>
                  </span>
                </a>
              </div>
            </div>
          </div>

          <div class="divider is-vertical is-hidden-touch">OR</div>
          <div class="divider is-hidden-desktop">OR</div>

          <div class="column">
            <div class="card">
              <div class="card-header">
                <div class="card-header-title">Claim a Proxy Character</div>
              </div>
              <div class="card-content">
                <p>These are Characters that are currently managed by the Team.</p>
                <p>If any of these are yours, just click them to attempt to claim and verify them as such!</p>
                <hr />
                <div class="box" v-if="teamProxies.length === 0">
                  <p>This team has no Proxy Characters, please sign up with one of your own!</p>
                </div>
                <a class="box" v-for="proxy in teamProxies" :key="proxy.id" @click="() => { claim(proxy.character) }">
                  <CharacterBio :character="proxy.character" :displayUnverified="false" />
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'
import CharacterBio from '@/components/character_bio.vue'
import ClaimCharacterModal from '@/components/modals/confirmations/claim_character.vue'
import TeamBio from '@/components/team/bio.vue'
import TeamMemberForm from '@/components/team/member_form.vue'
import { Character } from '@/interfaces/character'
import { TeamCreateResponse, TeamMemberUpdateErrors } from '@/interfaces/responses'
import Team from '@/interfaces/team'
import TeamMember from '@/interfaces/team_member'
import SavageAimMixin from '@/mixins/savage_aim_mixin'

@Component({
  components: {
    CharacterBio,
    TeamBio,
    TeamMemberForm,
  },
})
export default class TeamJoin extends SavageAimMixin {
  teamLoaded = false

  errors: TeamMemberUpdateErrors = {}

  team!: Team

  @Prop()
  teamId!: string

  // Values for sending
  get bisListId(): string {
    return (this.$refs.form as TeamMemberForm).bisListId
  }

  get characters(): Character[] {
    return this.$store.state.characters
  }

  get characterId(): string {
    return (this.$refs.form as TeamMemberForm).characterId
  }

  get teamProxies(): TeamMember[] {
    return this.team.members.filter((tm: TeamMember) => tm.character.proxy)
  }

  get url(): string {
    return `/backend/api/team/join/${this.teamId}/`
  }

  claim(character: Character): void {
    // Open the modal which will handle it all for us
    this.$modal.show(ClaimCharacterModal, { details: character, teamId: this.team.id, code: this.team.invite_code })
  }

  created(): void {
    this.fetchTeam(false)
  }

  async fetchTeam(reload: boolean): Promise<void> {
    // Load the team data from the API
    try {
      const response = await fetch(this.url)
      if (response.ok) {
        // Parse the JSON into a team and save it
        this.team = (await response.json()) as Team
        this.teamLoaded = true
        document.title = `Join ${this.team.name} - Savage Aim`
        if (reload) this.$forceUpdate()
      }
      else if (response.status === 404) {
        // Handle 404s ourselves to go back to the create/join page with a warning
        this.$router.push('/team/', () => {
          Vue.notify({ text: 'Invalid invite code! Please make sure you copied it correctly!', type: 'is-danger' })
        })
      }
      else {
        super.handleError(response.status)
      }
    }
    catch (e) {
      this.$notify({ text: `Error ${e} when fetching Team.`, type: 'is-danger' })
    }
  }

  async join(): Promise<void> {
    this.errors = {}

    const body = JSON.stringify({ bis_list_id: this.bisListId, character_id: this.characterId })
    try {
      const response = await fetch(this.url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': this.$cookies.get('csrftoken'),
        },
        body,
      })

      if (response.ok) {
        // Redirect back to the new bis list page
        const json = await response.json() as TeamCreateResponse
        this.$store.dispatch('fetchTeams')
        this.$router.push(`/team/${json.id}/`, () => {
          Vue.notify({ text: `Welcome to ${this.team.name}!`, type: 'is-success' })
        })
      }
      else {
        super.handleError(response.status)
        this.errors = (await response.json() as TeamMemberUpdateErrors)
      }
    }
    catch (e) {
      this.$notify({ text: `Error ${e} when attempting to create BIS List.`, type: 'is-danger' })
    }
  }

  async load(): Promise<void> {
    this.fetchTeam(true)
  }
}
</script>

<style lang="scss" scoped>
.columns .divider.is-vertical {
  margin: 0;
}
</style>
