<template>
  <div>
    <div class="card-header">
      <div class="card-header-title">Select a BIS List to load from.</div>
      <div class="card-header-icon">
        <a class="icon" @click="() => { this.$emit('close') }">
          <i class="material-icons">close</i>
        </a>
      </div>
    </div>
    <div class="card-content">
      <a @click="select(bis)" class="box" v-for="bis in bisLists" :key="bis.id">
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
                <img :src="`/job_icons/${bis.job.id}.webp`" :alt="`${bis.job.name} job icon`" width="24" height="24" />
              </span>
            </div>
          </div>
        </div>
      </a>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'
import BISList from '@/interfaces/bis_list'

@Component
export default class LoadCurrentGear extends Vue {
  @Prop()
  bisLists!: BISList[]

  @Prop()
  loadBIS!: (list: BISList) => void

  select(list: BISList): void {
    this.loadBIS(list)
    this.$emit('close')
  }
}
</script>
