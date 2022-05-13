<template>
  <div>
    <div class="card-header">
      <div class="card-header-title">{{ character.name }} - BIS Deletion</div>
      <div class="card-header-icon">
        <a @click="() => { this.$emit('close') }" class="icon">
          <i class="material-icons">close</i>
        </a>
      </div>
    </div>
    <div class="card-content">
      <h2 class="subtitle">Are you sure you want to delete this BIS List?</h2>
      <hr />
      <div class="box">
        <div class="level is-mobile">
          <div class="level-left">
            <div class="level-item">
              {{ bis.display_name }}
            </div>
          </div>
          <div class="level-right">
            <div class="level-item">
              <span class="tags has-addons">
                <span class="tag is-light">
                  iL
                </span>
                <span class="tag" :class="[`is-${bis.job.role}`]">
                  {{ bis.item_level }}
                </span>
              </span>
            </div>
            <div class="level-item">
              <span class="icon">
                <img :src="`/job_icons/${bis.job.name}.png`" :alt="`${bis.job.name} job icon`" width="24" height="24" />
              </span>
            </div>
          </div>
        </div>
      </div>
      <hr />
      <h2 class="subtitle">Deletion Eligibility</h2>
      <div v-if="loading">
        <button class="button is-static is-loading is-fullwidth">Loading</button>
      </div>
      <div class="content" v-else-if="details.length !== 0">
        <p class="has-text-warning">Cannot delete BIS List because it is in use in the following Teams;</p>
        <ul>
          <template v-for="team in details">
            <li :key="team.id">{{ team.name }} - <a @click="() => { editTeamBIS(team.id, team.member) }">Change</a></li>
          </template>
        </ul>
      </div>
      <div v-else>
        <p class="has-text-success">This BIS List is safe to delete!</p>
      </div>
    </div>
    <div class="card-footer">
      <a class="card-footer-item" @click="() => { this.$emit('close') }">Cancel</a>
      <a class="card-footer-item has-text-danger" v-if="canDelete" @click="deleteBIS">Delete</a>
      <p class="card-footer-item disabled-delete" v-else data-microtip-position="top" role="tooltip" aria-label="This BIS List is still in use.">Delete</p>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'
import BISList from '@/interfaces/bis_list'
import { CharacterDetails } from '@/interfaces/character'
import { BISListDeleteReadResponse } from '@/interfaces/responses'

@Component
export default class DeleteBIS extends Vue {
  @Prop()
  bis!: BISList

  @Prop()
  character!: CharacterDetails

  details: BISListDeleteReadResponse[] = []

  loading = true

  get canDelete(): boolean {
    return (!this.loading) && this.details.length === 0
  }

  get url(): string {
    return `/backend/api/character/${this.character.id}/bis_lists/${this.bis.id}/delete/`
  }

  mounted(): void {
    this.getDeleteInfo()
  }

  editTeamBIS(teamId: string, memberId: number): void {
    const url = `/team/${teamId}/member/${memberId}/`
    this.$emit('close')
    this.$router.push(url)
  }

  async getDeleteInfo(): Promise<void> {
    // Load the character data from the API
    try {
      const response = await fetch(this.url)
      if (response.ok) {
        // Parse the list into an array of character interfaces and store them in the character data list
        this.details = (await response.json()) as BISListDeleteReadResponse[]
        this.loading = false
      }
      else {
        this.$notify({ text: `Unexpected HTTP Error ${response.status} when fetching BIS List deletion results.`, type: 'is-danger' })
      }
    }
    catch (e) {
      this.$notify({ text: `Error ${e} when fetching BIS List deletion results.`, type: 'is-danger' })
    }
  }

  async deleteBIS(): Promise<void> {
    try {
      const response = await fetch(this.url, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': Vue.$cookies.get('csrftoken'),
        },
      })

      if (response.ok) {
        // Attempt to parse the json, get the id, and then redirect
        this.$emit('close')
        this.$notify({ text: `${this.bis.display_name} deleted successfully!`, type: 'is-success' })
      }
      else {
        this.$notify({ text: `Unexpected response ${response.status} when attempting to delete BIS List.`, type: 'is-danger' })
      }
    }
    catch (e) {
      this.$notify({ text: `Error ${e} when attempting to delete BIS List.`, type: 'is-danger' })
    }
  }
}
</script>
