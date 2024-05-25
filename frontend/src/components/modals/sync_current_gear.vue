<template>
  <div>
    <div class="card-header">
      <div class="card-header-title">Select BIS Lists to sync.</div>
      <div class="card-header-icon">
        <a class="icon" @click="() => { this.$emit('close') }">
          <i class="material-icons">close</i>
        </a>
      </div>
    </div>
    <div class="card-content">
      <a class="box" v-for="bis in bisLists" :key="bis.id" @click="(event) => { check(event, bis.id) }">
        <div class="level is-mobile">
          <div class="level-left">
            <div class="level-item">
              <input type="checkbox" :data-target="bis.id" ref="checkbox" />
            </div>
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
                <img :src="`/job_icons/${bis.job.id}.webp`" :alt="`${bis.job.name} job icon`" width="24" height="24" />
              </span>
            </div>
          </div>
        </div>
      </a>
    </div>
    <footer class="card-footer">
      <a class="card-footer-item has-text-success" @click="sync">
        <span class="icon-text">
          <span class="icon"><i class="material-icons">save_as</i></span>
          <span>{{ verb }} &amp; Sync</span>
        </span>
      </a>
      <a class="card-footer-item has-text-link" @click="() => { this.$emit('close') }">
        <span class="icon-text">
          <span class="icon"><i class="material-icons">close</i></span>
          <span>Cancel</span>
        </span>
      </a>
    </footer>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'
import BISList from '@/interfaces/bis_list'

@Component
export default class SyncCurrentGear extends Vue {
  @Prop()
  bisLists!: BISList[]

  @Prop()
  save!: (syncIds: string[]) => void

  @Prop()
  verb!: string

  check(e: MouseEvent, bisId: number): void {
    // First, ignore this function if the target was the checkbox
    if (e === null || (e.target as HTMLElement).tagName === 'INPUT') return
    // Find the checkbox that has the id as its data-target
    const checkbox = this.$el.querySelector(`input[data-target="${bisId}"]`) as HTMLInputElement | null
    if (checkbox === null) return
    checkbox.checked = !checkbox.checked
  }

  get checkboxes(): HTMLInputElement[] {
    return this.$refs.checkbox as HTMLInputElement[]
  }

  sync(): void {
    // Get the ids of the checked boxes and pass them back
    const toSync: string[] = []
    this.checkboxes.forEach((checkbox: HTMLInputElement) => {
      if (checkbox.checked) toSync.push(checkbox.dataset.target as string)
    })
    this.save(toSync)
    this.$emit('close')
  }
}
</script>
