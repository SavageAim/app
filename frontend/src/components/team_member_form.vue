<template>
  <div>
    <div class="field">
      <label class="label" for="character">Select Character</label>
      <div class="control">
        <div class="select is-fullwidth" :class="{'is-danger': characterIdErrors !== undefined}">
          <select v-model="characterId">
            <option value="-1">Select a Character</option>
            <option v-for="character in characters" :key="character.id" :value="character.id">{{ character.name }} @ {{ character.world }}</option>
          </select>
        </div>
      </div>
      <p v-if="characterIdErrors !== undefined" class="help is-danger">{{ characterIdErrors[0] }}</p>
      <p v-if="!characterVerified" class="help is-danger">This character hasn't been verified yet. Visit <router-link :to="`/characters/${characterId}/`">this page</router-link> to verify them!</p>
    </div>

    <div class="field">
      <label class="label" for="bis">Select BIS List</label>
      <div class="control has-icons-left">
        <template v-if="!bisListsLoaded">
          <div class="select is-fullwidth" :class="{'is-danger': bisListIdErrors !== undefined}">
            <select id="bis" disabled>
              <option value="-1">Select a Character first</option>
            </select>
          </div>
        </template>
        <template v-else>
          <div class="field has-addons">
            <div class="control is-expanded">
              <div class="select is-fullwidth">
                <select id="bis" v-model="bisListId">
                  <option value="-1">Select BIS List</option>
                  <option v-for="list in bisLists" :key="list.id" :data-target="list.job.name" :value="list.id">{{ list.display_name }}</option>
                </select>
              </div>
              <div class="icon is-small is-left" v-if="bisListId != -1">
                <img :src="`/job_icons/${bisIcon}.png`" :alt="`${bisIcon} job icon`" width="24" height="24" ref="jobIcon" />
              </div>
            </div>
            <div class="control">
              <a class="button is-link" target="_blank" @click="addBIS">Add New</a>
            </div>
          </div>
          <p v-if="bisListIdErrors !== undefined" class="help is-danger">{{ bisListIdErrors[0] }}</p>
        </template>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import {
  Component,
  Prop,
  Watch,
} from 'vue-property-decorator'
import AddBIS from '@/components/modals/add_bis.vue'
import BISList from '@/interfaces/bis_list'
import { Character, CharacterDetails } from '@/interfaces/character'
import SavageAimMixin from '@/mixins/savage_aim_mixin'

@Component
export default class TeamMemberForm extends SavageAimMixin {
  @Prop({ default: '-1' })
  initialBisListId!: string

  @Prop({ default: '-1' })
  initialCharacterId!: string

  @Prop({ default: undefined })
  bisListIdErrors!: string[] | undefined

  @Prop({ default: undefined })
  characterIdErrors!: string[] | undefined

  bisListsLoaded = false

  bisLists: BISList[] = []

  bisListId = this.initialBisListId

  characterId = this.initialCharacterId

  characterVerified = true

  refreshNote = false

  get bisIcon(): string {
    const list = this.bisLists.find((bl: BISList) => bl.id === parseInt(this.bisListId, 10))
    if (list != null) {
      return list.job.id
    }
    return ''
  }

  get characters(): Character[] {
    return this.$store.state.characters
  }

  get chosen(): Character | undefined {
    return this.characters.find((char: Character) => char.id === parseInt(this.characterId, 10))
  }

  addBIS(): void {
    this.$modal.show(AddBIS, { character: this.chosen }, { }, { closed: () => this.fetchBis() })
  }

  characterUrl(id: string): string {
    return `/backend/api/character/${id}/`
  }

  checkVerified(): void {
    // Check if the character we selected is verified or not
    if (this.characterId === '-1') {
      this.characterVerified = true
      return
    }

    // If it's an actual character we should check it in the list
    if (this.chosen != null) {
      this.characterVerified = this.chosen.verified
    }
  }

  @Watch('characterId')
  async fetchBis(): Promise<void> {
    // Whenever the character id is changed we should fetch the BIS Lists
    this.bisListsLoaded = false

    // Since we're not filtering out unverified users to be a bit more helpful to users, we should check verification here
    // Check it's an actual character
    this.checkVerified()
    if ((!this.characterVerified) || parseInt(this.characterId, 10) === -1) {
      this.bisLists = []
      return
    }

    // If not, go fetch the bis lists for the character
    const url = this.characterUrl(this.characterId)
    try {
      const response = await fetch(url)
      if (response.ok) {
        // Parse the list into an array of character interfaces and store them in the character data list
        const details = (await response.json()) as CharacterDetails
        this.bisLists = details.bis_lists
        this.bisListsLoaded = true
      }
      else {
        super.handleError(response.status)
      }
    }
    catch (e) {
      this.$notify({ text: `Error ${e} when fetching BIS Lists for the chosen Character.`, type: 'is-danger' })
    }
  }

  mounted(): void {
    if (this.initialCharacterId !== '-1') this.fetchBis()
  }
}
</script>

<style lang="scss">
.field:last-child {
  margin-bottom: 0.75rem!important;
}
</style>
