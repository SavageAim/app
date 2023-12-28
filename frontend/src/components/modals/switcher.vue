<template>
  <div>
    <div class="card-header">
      <div class="card-header-title">
        Quick Switcher
      </div>
      <div class="card-header-icon">
        <a class="icon" @click="() => { this.$emit('close') }">
          <i class="material-icons">close</i>
        </a>
      </div>
    </div>
    <div class="card-content">
      <input
        class="input"
        id="searchbox"
        ref="searchbox"
        type="url"
        placeholder="Search for Teams, Characters, or BIS Lists"
        v-shortkey="{up: ['arrowup'], down: ['arrowdown'], select: ['enter']}"
        @shortkey="handleShortkey"
        autocomplete="off"
        v-model="searchTerm"
      />

      <article class="panel is-link" id="link-chooser" :key="currentChoices.length">
        <a v-for="(choice, index) in currentChoices" class="panel-block" :class="{'is-active': index === targetIndex}" :key="choice.url" @click="() => { open(choice.url) }">
          <div class="panel-icon">
            <i class="material-icons" aria-hidden="true">{{ choice.iconName }}</i>
          </div>
          <span>{{ choice.name }}</span>
        </a>
      </article>
    </div>
  </div>
</template>

<script lang="ts">
// import * as Sentry from '@sentry/vue'
import { matchSorter } from 'match-sorter'
import { Component, Vue, Watch } from 'vue-property-decorator'
import BISList from '@/interfaces/bis_list'
import { CharacterDetails } from '@/interfaces/character'
import Team from '@/interfaces/team'
import TeamMember from '@/interfaces/team_member'

interface SwitcherItem {
  iconName: string
  name: string
  url: string
}

@Component
export default class QuickSwitcher extends Vue {
  currentChoices: SwitcherItem[] = []

  searchTerm = ''

  targetIndex = 0

  close(): void {
    this.$emit('close')
  }

  get potentialChoices(): SwitcherItem[] {
    const choices: SwitcherItem[] = this.$store.state.characters.map(
      (char: CharacterDetails) => [
        {
          iconName: 'person',
          name: char.name,
          url: `/characters/${char.id}/`,
        },
        ...char.bis_lists.map(
          (bis: BISList) => ({
            iconName: 'list_alt',
            name: `${char.name} / ${bis.name}`,
            url: `/characters/${char.id}/bis_list/${bis.id}/`,
          }),
        ),
      ],
    ).flat()

    // For team stuff, since we have to check permissions before pushing certain pages
    this.$store.state.teams.forEach((team: Team) => {
      choices.push({
        iconName: 'group',
        name: team.name,
        url: `/team/${team.id}/`,
      })
      choices.push({
        iconName: 'receipt_long',
        name: `${team.name} / Loot Manager`,
        url: `/team/${team.id}/loot/`,
      })
      choices.push({
        iconName: 'manage_accounts',
        name: `${team.name} / Manage Members`,
        url: `/team/${team.id}/management/`,
      })

      if (team.members.find((member: TeamMember) => member.lead)!.character.user_id === this.$store.state.user.id) {
        choices.push({
          iconName: 'settings',
          name: `${team.name} / Settings`,
          url: `/team/${team.id}/settings/`,
        })
      }
    })

    return choices
  }

  get searchbox(): HTMLInputElement {
    return this.$refs.searchbox as HTMLInputElement
  }

  @Watch('searchTerm')
  checkInput(): void {
    this.targetIndex = 0
    if (this.searchTerm === '') {
      this.currentChoices = matchSorter(this.potentialChoices, this.searchTerm, { keys: ['name'] }).filter((item: SwitcherItem) => item.name.indexOf('/') === -1)
    }
    else {
      this.currentChoices = matchSorter(this.potentialChoices, this.searchTerm, { keys: ['name'] }).slice(0, 5)
    }
  }

  mounted(): void {
    // Compile the list of initial currentChoices
    this.checkInput()

    this.searchbox.focus()
  }

  handleShortkey(event: { srcKey: string }): void {
    switch (event.srcKey) {
    case 'up':
      // Decrement by 1, wrap around
      this.targetIndex = (this.targetIndex - 1 + this.currentChoices.length) % this.currentChoices.length
      break
    case 'down':
      // Increment by 1, wrap around
      this.targetIndex = (this.targetIndex + 1) % this.currentChoices.length
      break
    case 'select':
      this.open(this.currentChoices[this.targetIndex].url)
      break
    default:
      break
    }
  }

  async open(url: string): Promise<void> {
    // Route to the given URL and close the switcher
    await this.$router.push(url)
    this.$emit('close')
  }
}
</script>

<style lang="scss">
#link-chooser .panel-icon {
  font-size: 24px;
  margin-right: 0.3em;
}
</style>
