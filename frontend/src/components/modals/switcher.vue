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
      />

      <article class="panel is-link" id="link-chooser">
        <a v-for="(choice, index) in choices" class="panel-block" :class="{'is-active': index === targetIndex}" :key="choice.url" @click="() => { open(choice.url) }">
          <div class="panel-icon">
            <i class="material-icons" aria-hidden="true" v-if="choice.isTeam">group</i>
            <i class="material-icons" aria-hidden="true" v-else>person</i>
          </div>
          <span>{{ choice.name }}</span>
        </a>
      </article>
    </div>
  </div>
</template>

<script lang="ts">
// import * as Sentry from '@sentry/vue'
import { Component, Vue } from 'vue-property-decorator'
import { Character } from '@/interfaces/character'
import Team from '@/interfaces/team'

interface SwitcherItem {
  name: string
  url: string
  isTeam: boolean
}

@Component
export default class QuickSwitcher extends Vue {
  choices: SwitcherItem[] = []

  targetIndex = 0

  close(): void {
    this.$emit('close')
  }

  get searchbox(): HTMLInputElement {
    return this.$refs.searchbox as HTMLInputElement
  }

  mounted(): void {
    // Compile the list of initial choices
    this.choices = [
      ...this.$store.state.characters.map((char: Character) => ({ name: char.name, url: `/characters/${char.id}`, isTeam: false })),
      ...this.$store.state.teams.map((team: Team) => ({ name: team.name, url: `/team/${team.id}`, isTeam: true })),
    ]

    this.searchbox.focus()
  }

  handleShortkey(event: { srcKey: string }): void {
    switch (event.srcKey) {
    case 'up':
      // Decrement by 1, wrap around
      this.targetIndex = (this.targetIndex - 1 + this.choices.length) % this.choices.length
      break
    case 'down':
      // Increment by 1, wrap around
      this.targetIndex = (this.targetIndex + 1) % this.choices.length
      break
    case 'select':
      this.open(this.choices[this.targetIndex].url)
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
