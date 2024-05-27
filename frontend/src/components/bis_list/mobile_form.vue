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
          <Filters :minIl="minIl" :maxIl="maxIl" v-on="$listeners" />
        </div>
      </div>

      <div v-if="tabsShown.details">
        <div class="card">
          <Details :bisList="bisList" :char-is-proxy="charIsProxy" :errors="errors" v-on="$listeners" />
        </div>
      </div>

      <div v-if="tabsShown.bis">
        <div class="card">
          <BIS :bisList="bisList" :errors="errors" :minIl="minIl" :maxIl="maxIl" :displayOffhand="displayOffhand" />
          <div class="card-footer">
            <p class="card-footer-item is-loading" v-if="importLoading"></p>
            <a class="card-footer-item" v-else-if="etroImportable" @click="importBis">
              <span class="icon-text">
                <span class="icon"><i class="material-icons">cloud_download</i></span>
                <span>Import from Etro</span>
              </span>
            </a>
            <p class="card-footer-item" v-else data-microtip-position="bottom" role="tooltip" aria-label="Please enter an Etro gearset link in the gearset's URL field.">
              <span class="icon-text">
                <span class="icon"><i class="material-icons">cloud_off</i></span>
                <span>Import from Etro</span>
              </span>
            </p>
          </div>
        </div>
      </div>

      <div v-if="tabsShown.current">
        <div class="card">
          <Current :bisList="bisList" :errors="errors" :minIl="minIl" :maxIl="maxIl" :displayOffhand="displayOffhand" />

          <div class="card-footer">
            <p class="card-footer-item is-loading" v-if="importLoading"></p>
            <a class="card-footer-item has-text-link" v-else @click="importLodestone">
              <span class="icon-text">
                <span class="icon"><i class="material-icons">cloud_download</i></span>
                <span v-if="displayCopy">Lodestone</span>
                <span v-else>Import from Lodestone</span>
              </span>
            </a>

            <template v-if="displayCopy">
              <a class="card-footer-item has-text-link" v-if="syncable" data-microtip-position="top" role="tooltip" :aria-label="`Load Current gear from another ${bisList.job_id} BIS List.`" @click="importFromOtherList">
                <span class="icon-text">
                  <span class="icon"><i class="material-icons">content_copy</i></span>
                  <span>Other List</span>
                </span>
              </a>
              <p class="card-footer-item" v-else data-microtip-position="top" role="tooltip" :aria-label="`You have no other ${bisList.job_id} BIS Lists.`">
                <span class="icon-text">
                  <span class="icon"><i class="material-icons">content_copy</i></span>
                  <span>Other List</span>
                </span>
              </p>
            </template>
          </div>
        </div>
      </div>

      <!-- Actions -->
      <div class="card mobile-actions">
        <Actions :bisList="bisList" :character="character" :char-is-proxy="charIsProxy" :url="url" :method="method" v-on="$listeners" :simple="simpleActions" />
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
import { CharacterDetails } from '@/interfaces/character'
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
  character!: CharacterDetails

  @Prop()
  charIsProxy!: boolean

  @Prop()
  displayOffhand!: boolean

  @Prop()
  errors!: BISListErrors

  @Prop()
  etroImportable!: boolean

  @Prop()
  importLoading!: boolean

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
  syncable!: boolean

  @Prop()
  url!: string

  get displayCopy(): boolean {
    return !(this.simpleActions || this.charIsProxy)
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

  importBis(): void {
    this.$emit('import-bis-data')
  }

  importFromOtherList(): void {
    this.$emit('import-current-data')
  }

  importLodestone(): void {
    this.$emit('import-current-lodestone-gear')
  }
}
</script>

<style lang="scss">
.mobile-actions {
  margin-top: 2rem;
}
</style>
