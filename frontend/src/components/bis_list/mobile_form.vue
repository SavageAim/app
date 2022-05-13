<template>
  <div>
    <div class="mobile-form">
      <div class="tabs is-fullwidth is-boxed">
        <ul>
          <li :class="{ 'is-active': tabsShown.filters }">
            <a @click="showFilters">
              <span>Filters</span>
            </a>
          </li>
          <li :class="{ 'is-active': tabsShown.details }">
            <a @click="showDetails" class="icon-text">
              <span class="icon has-text-danger" v-if="detailsTabHasErrors"><i class="material-icons">warning</i></span>
              <span>Details</span>
            </a>
          </li>
          <li :class="{ 'is-active': tabsShown.bis }">
            <a @click="showBIS" class="icon-text">
              <span class="icon has-text-danger" v-if="bisTabHasErrors"><i class="material-icons">warning</i></span>
              <span>BIS</span>
            </a>
          </li>
          <li :class="{ 'is-active': tabsShown.current }">
            <a @click="showCurrent" class="icon-text">
              <span class="icon has-text-danger" v-if="currentTabHasErrors"><i class="material-icons">warning</i></span>
              <span>Current</span>
            </a>
          </li>
        </ul>
      </div>

      <!-- Filters -->
      <div v-if="tabsShown.filters">
        <div class="card">
          <Filters :minIl="minIl" :maxIl="maxIl" v-on:update-min="updateMin" v-on:update-max="updateMax" />
        </div>
      </div>

      <div v-if="tabsShown.details">
        <div class="card">
          <Details :bisList="bisList" :errors="errors" v-on:job-change="jobChange" />
        </div>
      </div>

      <div v-if="tabsShown.bis">
        <div class="card">
          <BIS :bisList="bisList" :errors="errors" :minIl="minIl" :maxIl="maxIl" :displayOffhand="displayOffhand" />
        </div>
      </div>

      <div v-if="tabsShown.current">
        <div class="card">
          <Current :bisList="bisList" :errors="errors" :minIl="minIl" :maxIl="maxIl" :displayOffhand="displayOffhand" />
        </div>
      </div>

      <!-- Actions -->
      <div class="card mobile-actions">
        <div class="card-header">
          <div class="card-header-title">
            <span>Actions</span>
          </div>
        </div>

        <Actions :bisList="bisList" :url="url" :method="method" v-on="$listeners" :simple="simpleActions" />
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'
import Actions from '@/components/bis_list/actions.vue'
import BIS from '@/components/bis_list/bis.vue'
import Current from '@/components/bis_list/current.vue'
import Details from '@/components/bis_list/details.vue'
import Filters from '@/components/bis_list/filters.vue'
import BISListModify from '@/dataclasses/bis_list_modify'
import { BISListErrors } from '@/interfaces/responses'

@Component({
  components: {
    Actions,
    BIS,
    Current,
    Details,
    Filters,
  },
})
export default class BISListMobileForm extends Vue {
  tabsShown = {
    bis: false,
    current: false,
    details: true,
    filters: false,
  }

  @Prop()
  bisList!: BISListModify

  @Prop()
  displayOffhand!: boolean

  @Prop()
  errors!: BISListErrors

  // Set up default values for min and max IL, will change as new tiers are released
  @Prop()
  maxIl!: number

  @Prop()
  method!: string

  @Prop()
  minIl!: number

  // Hide actions that spawn a popup, when used in the add bis section
  @Prop()
  simpleActions!: boolean

  @Prop()
  url!: string

  jobChange(selectedJob: string): void {
    this.$emit('job-change', selectedJob)
  }

  updateMin(minIl: number): void {
    this.$emit('update-min-il', minIl)
  }

  updateMax(maxIl: number): void {
    this.$emit('update-max-il', maxIl)
  }

  // Method toggle for the tabs
  showBIS(): void {
    this.showNone()
    this.tabsShown.bis = true
  }

  showCurrent(): void {
    this.showNone()
    this.tabsShown.current = true
  }

  showDetails(): void {
    this.showNone()
    this.tabsShown.details = true
  }

  showFilters(): void {
    this.showNone()
    this.tabsShown.filters = true
  }

  // Reset the object
  showNone(): void {
    this.tabsShown.current = false
    this.tabsShown.bis = false
    this.tabsShown.details = false
    this.tabsShown.filters = false
  }

  // Functions to indicate if a tab has errors
  get bisTabHasErrors(): boolean {
    return (
      this.errors.bis_mainhand_id !== undefined
      || this.errors.bis_offhand_id !== undefined
      || this.errors.bis_head_id !== undefined
      || this.errors.bis_body_id !== undefined
      || this.errors.bis_hands_id !== undefined
      || this.errors.bis_legs_id !== undefined
      || this.errors.bis_feet_id !== undefined
      || this.errors.bis_earrings_id !== undefined
      || this.errors.bis_necklace_id !== undefined
      || this.errors.bis_bracelet_id !== undefined
      || this.errors.bis_right_ring_id !== undefined
      || this.errors.bis_left_ring_id !== undefined
    )
  }

  get currentTabHasErrors(): boolean {
    return (
      this.errors.current_mainhand_id !== undefined
      || this.errors.current_offhand_id !== undefined
      || this.errors.current_head_id !== undefined
      || this.errors.current_body_id !== undefined
      || this.errors.current_hands_id !== undefined
      || this.errors.current_legs_id !== undefined
      || this.errors.current_feet_id !== undefined
      || this.errors.current_earrings_id !== undefined
      || this.errors.current_necklace_id !== undefined
      || this.errors.current_bracelet_id !== undefined
      || this.errors.current_right_ring_id !== undefined
      || this.errors.current_left_ring_id !== undefined
    )
  }

  get detailsTabHasErrors(): boolean {
    return (
      this.errors.job_id !== undefined
      || this.errors.external_link !== undefined
    )
  }
}
</script>

<style lang="scss">
.mobile-actions {
  margin-top: 2rem;
}
</style>
