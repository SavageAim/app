<template>
  <div class="columns is-desktop">
    <div class="column is-three-quarters-desktop">
      <div class="card">
        <div class="card-header">
          <div class="card-header-title"><span class="larger-title">Your Teams</span></div>
          <div class="card-header-icon">
            <router-link to="/team/" class="button is-small is-success">
              <span class="icon"><i class="material-icons">add</i></span>
              <span>Add New</span>
            </router-link>
          </div>
        </div>
        <div class="card-content">
          <template v-if="teams.length === 0">
            <p class="has-text-centered">No teams found.</p>
          </template>
          <template v-else>
            <router-link v-for="team in teams" :key="team.id" class="box" :to="`/team/${team.id}/`">
              <TeamBio :team="team" />
            </router-link>
          </template>
        </div>
      </div>
    </div>

    <div class="column">
    <div class="card">
      <div class="card-header">
        <div class="card-header-title"><span class="larger-title">Your Characters</span></div>
        <div class="card-header-icon">
          <router-link to="/characters/new/" class="button is-small is-success">
            <span class="icon"><i class="material-icons">add</i></span>
            <span>Add New</span>
          </router-link>
        </div>
      </div>
      <div class="card-content">
        <!-- If no characters loaded, display a message, otherwise make a forloop -->
        <template v-if="characters.length === 0">
          <p class="has-text-centered">No characters found.</p>
        </template>
        <template v-else>
          <router-link :to="`/characters/${char.id}/`" v-for="char in characters" :key="char.id" class="box">
            <CharacterBio :character="char" />
          </router-link>
        </template>
      </div>
    </div>
  </div>
  </div>
</template>

<script lang="ts">
import { Component } from 'vue-property-decorator'
import CharacterBio from '@/components/character_bio.vue'
import TeamBio from '@/components/team/bio.vue'
import { Character } from '@/interfaces/character'
import Team from '@/interfaces/team'
import SavageAimMixin from '@/mixins/savage_aim_mixin'

@Component({
  components: {
    CharacterBio,
    TeamBio,
  },
})
export default class Dashboard extends SavageAimMixin {
  get characters(): Character[] {
    return this.$store.state.characters
  }

  get teams(): Team[] {
    return this.$store.state.teams
  }

  mounted(): void {
    this.$store.dispatch('fetchCharacters')
    this.$store.dispatch('fetchTeams')
  }
}
</script>

<style lang="scss">
</style>
