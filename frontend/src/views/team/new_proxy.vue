<template>
  <div>
    <div v-if="loading">
      <button class="button is-static is-loading is-fullwidth">Loading</button>
    </div>

    <template v-else>
      <div class="breadcrumb">
        <ul>
          <li><router-link :to="`/team/${team.id}/`">{{ team.name }}</router-link></li>
          <li class="is-active"><a href="#">Proxy Characters</a></li>
          <li class="is-active"><a aria-current="page">New</a></li>
        </ul>
      </div>

      <div class="card">
        <div class="card-content">
          <CharacterForm :api-errors="characterApiErrors" :api-loading="requesting" @fetched="updateChar" v-if="character === null" />
          <template v-else>
            <div class="box" id="char-box">
              <CharacterBio :character="character" :displayUnverified="false" />
            </div>
            <div class="field has-addons">
              <div class="control is-expanded">
                <button class="button is-danger is-fullwidth" @click="() => { this.character = null }">Change Character</button>
              </div>
              <div class="control is-expanded">
                <button class="button is-success is-fullwidth">Create Proxy</button>
              </div>
            </div>
          </template>
        </div>
      </div>

      <BISListForm :bisList="bis" :character="character" :url="''" method="" v-if="character !== null" :char-is-proxy="true" />
    </template>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import BISListForm from '@/components/bis_list/form.vue'
import CharacterBio from '@/components/character_bio.vue'
import CharacterForm from '@/components/character_form.vue'
import BISListModify from '@/dataclasses/bis_list_modify'
import { Character } from '@/interfaces/character'
import Team from '@/interfaces/team'
import TeamMember from '@/interfaces/team_member'
import { BISListErrors } from '@/interfaces/responses'
import SavageAimMixin from '@/mixins/savage_aim_mixin'

@Component({
  components: {
    BISListForm,
    CharacterBio,
    CharacterForm,
  },
})
export default class NewProxy extends SavageAimMixin {
  bis = new BISListModify()

  bisAPIErrors: BISListErrors = {}

  character: Character | null = null

  characterApiErrors: string[] = []

  loading = true

  requesting = false

  team!: Team

  // Flag stating whether the currently logged user can edit the Team
  get editable(): boolean {
    return this.team.members.find((teamMember: TeamMember) => teamMember.character.user_id === this.$store.state.user.id)?.lead ?? false
  }

  get url(): string {
    return `/backend/api/team/${this.$route.params.id}/`
  }

  checkPermissions(): void {
    // Ensure that the person on this page is the team leader and not anybody else
    if (!this.editable) {
      this.$router.push(`/team/${this.team.id}/`, () => {
        Vue.notify({ text: 'Only the team leader can manage proxies.', type: 'is-warning' })
      })
    }
  }

  created(): void {
    this.fetchTeam(false)
  }

  updateChar(char: Character): void {
    this.character = char
  }

  // API Interaction
  async fetchTeam(reload: boolean): Promise<void> {
    // Load the team data from the API
    try {
      const response = await fetch(this.url)
      if (response.ok) {
        // Parse the JSON into a team and save it
        this.team = (await response.json()) as Team
        this.checkPermissions()
        this.loading = false
        if (reload) this.$forceUpdate()
        document.title = `New Proxy - ${this.team.name} - Savage Aim`
      }
      else {
        super.handleError(response.status)
      }
    }
    catch (e) {
      this.$notify({ text: `Error ${e} when fetching Team.`, type: 'is-danger' })
    }
  }

  async load(): Promise<void> {
    this.fetchTeam(true)
  }
}
</script>

<style lang="scss">
#char-box {
  margin-bottom: 0;
}
</style>
