<template>
  <div class="card-content">
  <div class="field is-horizontal" v-if="!charIsProxy">
    <div class="field-label is-normal">
      <label class="label">Name</label>
    </div>
    <div class="field-body">
      <div class="field">
        <div class="control">
          <input class="input" :class="{'is-danger': errors.name !== undefined}" v-model="bisList.name" placeholder="" />
        </div>
        <p v-if="errors.name !== undefined" class="help is-danger">{{ errors.name[0] }}</p>
      </div>
    </div>
  </div>

  <div class="field is-horizontal">
    <div class="field-label is-normal">
      <label class="label">Job</label>
    </div>
    <div class="field-body">
      <div class="field">
        <div class="control has-icons-left">
          <div class="select is-fullwidth" :class="{'is-danger': errors.job_id !== undefined}">
            <select ref="jobPicker" @change="changeJob" v-model="bisList.job_id">
              <option v-for="job in jobs" :key="job.name" :value="job.id">{{ job.display_name }}</option>
            </select>
          </div>
          <div class="icon is-small is-left">
            <img :src="`/job_icons/${bisList.job_id}.png`" :alt="`${bisList.job_id} Job Icon`" width="24" height="24" ref="jobIcon" />
          </div>
        </div>
        <p v-if="errors.job_id !== undefined" class="help is-danger">{{ errors.job_id[0] }}</p>
      </div>
    </div>
  </div>

  <div class="field is-horizontal">
    <div class="field-label is-normal">
      <label class="label">Extra URL</label>
    </div>
    <div class="field-body">
      <div class="field">
        <div class="control">
          <input class="input" :class="{'is-danger': errors.external_link !== undefined}" v-model="bisList.external_link" placeholder="i.e. Etro, Ariyala, etc" />
        </div>
        <p v-if="errors.external_link !== undefined" class="help is-danger">{{ errors.external_link[0] }}</p>
        <p class="help is-info" v-else>Etro links can now be imported automatically!</p>
      </div>
    </div>
  </div>
</div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'
import BISListModify from '@/dataclasses/bis_list_modify'
import { BISListErrors } from '@/interfaces/responses'
import Job from '@/interfaces/job'

@Component
export default class Details extends Vue {
  baseImgUrl = '/job_icons/'

  displayOffhand = true

  @Prop()
  bisList!: BISListModify

  @Prop()
  charIsProxy!: boolean

  @Prop()
  errors!: BISListErrors

  get jobs(): Job[] {
    return this.$store.state.jobs
  }

  // Conversion getters for job related refs
  get jobIcon(): HTMLImageElement {
    return this.$refs.jobIcon as HTMLImageElement
  }

  get jobPicker(): HTMLSelectElement {
    return this.$refs.jobPicker as HTMLSelectElement
  }

  changeJob(): void {
    const selectedJob = (this.jobPicker.options[this.jobPicker.selectedIndex]).value as string

    // Handle the flag for the offhand
    this.$emit('job-change', selectedJob)
  }
}
</script>
