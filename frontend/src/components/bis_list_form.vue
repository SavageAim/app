<template>
  <div class="columns is-dekstop">
    <div class="column">
      <div class="card">
        <div class="card-header">
          <div class="card-header-title">
            <span>Details</span>
          </div>
        </div>

        <div class="card-content">
          <div class="field is-horizontal">
            <div class="field-label is-normal">
              <label class="label">Job</label>
            </div>
            <div class="field-body">
              <div class="field">
                <div class="control has-icons-left">
                  <div class="select is-fullwidth" :class="{'is-danger': errors.job_id !== undefined}">
                    <select ref="jobPicker" @change="changeJobIcon" v-model="bisList.job_id">
                      <option value="na" disabled data-target="paladin">Select a Job</option>
                      <option v-for="job in jobs" :key="job.name" :data-target="job.name" :value="job.id">{{ job.display_name }}</option>
                    </select>
                  </div>
                  <div class="icon is-small is-left">
                    <img src="/job_icons/paladin.png" alt="Paladin Job Icon" width="24" height="24" ref="jobIcon" />
                  </div>
                </div>
                <p v-if="errors.job_id !== undefined" class="help is-danger">{{ errors.job_id[0] }}</p>
              </div>
            </div>
          </div>

          <div class="field is-horizontal">
            <div class="field-label is-normal">
              <label class="label">URL</label>
            </div>
            <div class="field-body">
              <div class="field">
                <div class="control">
                  <input class="input" :class="{'is-danger': errors.external_link !== undefined}" v-model="bisList.external_link" />
                </div>
                <p v-if="errors.external_link !== undefined" class="help is-danger">{{ errors.external_link[0] }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Filters -->
      <div class="card">
        <div class="card-header">
          <div class="card-header-title">
            <span>Filters</span>
          </div>
        </div>

        <div class="card-content">
          <p class="subtitle">Item Level Range</p>
          <div class="field is-horizontal">
            <div class="field-label is-normal">
              <label class="label">Min</label>
            </div>
            <div class="field-body">
              <div class="field">
                <div class="control">
                  <div class="select is-fullwidth">
                    <select ref="minIlPicker" v-model="minIl">
                      <option v-for="val in ilChoices" :key="val" :value="val">{{ val }}</option>
                    </select>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="field is-horizontal">
            <div class="field-label is-normal">
              <label class="label">Max</label>
            </div>
            <div class="field-body">
              <div class="field">
                <div class="control">
                  <div class="select is-fullwidth">
                    <select ref="maxIlPicker" v-model="maxIl">
                      <option v-for="val in ilChoices" :key="val" :value="val">{{ val }}</option>
                    </select>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="column">
      <div class="card">
        <div class="card-header">
          <div class="card-header-title">
            <span>BIS Gear</span>
          </div>
        </div>
        <div class="card-content">
          <GearDropdown :maxIl="maxIl" :minIl="minIl" ref="bisMainhand" name="Main Hand" :choices="weapons" v-model="bisList.bis_mainhand_id" :error="errors.bis_mainhand_id" />
          <GearDropdown :maxIl="maxIl" :minIl="minIl" ref="bisOffhand" name="Off Hand" :choices="weapons" v-if="displayOffhand" v-model="bisList.bis_offhand_id" :error="errors.bis_offhand_id" />
          <GearDropdown :maxIl="maxIl" :minIl="minIl" ref="bisHead" name="Head" :choices="armour" v-model="bisList.bis_head_id" :error="errors.bis_head_id" />
          <GearDropdown :maxIl="maxIl" :minIl="minIl" ref="bisBody" name="Body" :choices="armour" v-model="bisList.bis_body_id" :error="errors.bis_body_id" />
          <GearDropdown :maxIl="maxIl" :minIl="minIl" ref="bisHands" name="Hands" :choices="armour" v-model="bisList.bis_hands_id" :error="errors.bis_hands_id" />
          <GearDropdown :maxIl="maxIl" :minIl="minIl" ref="bisLegs" name="Legs" :choices="armour" v-model="bisList.bis_legs_id" :error="errors.bis_legs_id" />
          <GearDropdown :maxIl="maxIl" :minIl="minIl" ref="bisFeet" name="Feet" :choices="armour" v-model="bisList.bis_feet_id" :error="errors.bis_feet_id" />
          <GearDropdown :maxIl="maxIl" :minIl="minIl" ref="bisEarrings" name="Earrings" :choices="accessories" v-model="bisList.bis_earrings_id" :error="errors.bis_earrings_id" />
          <GearDropdown :maxIl="maxIl" :minIl="minIl" ref="bisNecklace" name="Necklace" :choices="accessories" v-model="bisList.bis_necklace_id" :error="errors.bis_necklace_id" />
          <GearDropdown :maxIl="maxIl" :minIl="minIl" ref="bisBracelet" name="Bracelet" :choices="accessories" v-model="bisList.bis_bracelet_id" :error="errors.bis_bracelet_id" />
          <GearDropdown :maxIl="maxIl" :minIl="minIl" ref="bisRightRing" name="Right Ring" :choices="accessories" v-model="bisList.bis_right_ring_id" :error="errors.bis_right_ring_id" />
          <GearDropdown :maxIl="maxIl" :minIl="minIl" ref="bisLeftRing" name="Left Ring" :choices="accessories" v-model="bisList.bis_left_ring_id" :error="errors.bis_left_ring_id" />
        </div>
      </div>
    </div>

    <div class="column">
      <div class="card">
        <div class="card-header">
          <div class="card-header-title">
            <span>Current Gear</span>
          </div>
        </div>
        <div class="card-content">
          <GearDropdown :maxIl="maxIl" :minIl="minIl" ref="currMainhand" name="Main Hand" :choices="weapons" v-model="bisList.current_mainhand_id" :error="errors.current_mainhand_id" />
          <GearDropdown :maxIl="maxIl" :minIl="minIl" ref="currOffhand" name="Off Hand" :choices="weapons" v-if="displayOffhand" v-model="bisList.current_offhand_id" :error="errors.current_offhand_id" />
          <GearDropdown :maxIl="maxIl" :minIl="minIl" ref="currHead" name="Head" :choices="armour" v-model="bisList.current_head_id" :error="errors.current_head_id" />
          <GearDropdown :maxIl="maxIl" :minIl="minIl" ref="currBody" name="Body" :choices="armour" v-model="bisList.current_body_id" :error="errors.current_body_id" />
          <GearDropdown :maxIl="maxIl" :minIl="minIl" ref="currHands" name="Hands" :choices="armour" v-model="bisList.current_hands_id" :error="errors.current_hands_id" />
          <GearDropdown :maxIl="maxIl" :minIl="minIl" ref="currLegs" name="Legs" :choices="armour" v-model="bisList.current_legs_id" :error="errors.current_legs_id" />
          <GearDropdown :maxIl="maxIl" :minIl="minIl" ref="currFeet" name="Feet" :choices="armour" v-model="bisList.current_feet_id" :error="errors.current_feet_id" />
          <GearDropdown :maxIl="maxIl" :minIl="minIl" ref="currEarrings" name="Earrings" :choices="accessories" v-model="bisList.current_earrings_id" :error="errors.current_earrings_id" />
          <GearDropdown :maxIl="maxIl" :minIl="minIl" ref="currNecklace" name="Necklace" :choices="accessories" v-model="bisList.current_necklace_id" :error="errors.current_necklace_id" />
          <GearDropdown :maxIl="maxIl" :minIl="minIl" ref="currBracelet" name="Bracelet" :choices="accessories" v-model="bisList.current_bracelet_id" :error="errors.current_bracelet_id" />
          <GearDropdown :maxIl="maxIl" :minIl="minIl" ref="currRightRing" name="Right Ring" :choices="accessories" v-model="bisList.current_right_ring_id" :error="errors.current_right_ring_id" />
          <GearDropdown :maxIl="maxIl" :minIl="minIl" ref="currLeftRing" name="Left Ring" :choices="accessories" v-model="bisList.current_left_ring_id" :error="errors.current_left_ring_id" />
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'
import range from 'range-inclusive'
import GearDropdown from './gear_dropdown.vue'
import BISListModify from '@/dataclasses/bis_list_modify'
import { BISListErrors } from '@/interfaces/responses'
import Gear from '@/interfaces/gear'
import Job from '@/interfaces/job'

@Component({
  components: {
    GearDropdown,
  },
})
export default class BISListForm extends Vue {
  baseImgUrl = '/job_icons/'

  displayOffhand = true

  @Prop()
  bisList!: BISListModify

  @Prop()
  errors!: BISListErrors

  @Prop()
  jobs!: Job[]

  // Set up default values for min and max IL, will change as new tiers are released
  maxIl = 605

  minIl = 580

  // Filtered array of gear for accessories
  get accessories(): Gear[] {
    return this.gear.filter((item: Gear) => item.has_accessories)
  }

  // Filtered array of gear for armour
  get armour(): Gear[] {
    return this.gear.filter((item: Gear) => item.has_armour)
  }

  // Get gear from store
  get gear(): Gear[] {
    return this.$store.state.gear
  }

  // Get an array of item level choices based on the total min and max values
  get ilChoices(): number[] {
    return range(this.$store.state.maxItemLevel, this.$store.state.minItemLevel, -5)
  }

  // Conversion getters for job related refs
  get jobIcon(): HTMLImageElement {
    return this.$refs.jobIcon as HTMLImageElement
  }

  get jobPicker(): HTMLSelectElement {
    return this.$refs.jobPicker as HTMLSelectElement
  }

  // Filtered array of gear for weapons
  get weapons(): Gear[] {
    return this.gear.filter((item: Gear) => item.has_weapon)
  }

  // On mount, run the changeJob icon function to update for edit pages
  mounted(): void {
    this.changeJobIcon()
  }

  // Update job icons when the job dropdown changes
  changeJobIcon(): void {
    const selectedJob = (this.jobPicker.options[this.jobPicker.selectedIndex]).dataset.target

    // Handle the flag for the offhand
    this.displayOffhand = selectedJob === 'paladin'

    this.jobIcon.src = `${this.baseImgUrl}${selectedJob}.png`
    this.jobIcon.alt = `${selectedJob} job icon`
  }
}
</script>

<style lang="scss">
</style>
