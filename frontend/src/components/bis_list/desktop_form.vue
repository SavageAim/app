<template>
  <div class="columns is-hidden-touch">
    <div class="column">
      <div class="card">
        <div class="card-header">
          <div class="card-header-title">
            <span>Details</span>
          </div>
        </div>

        <Details :bisList="bisList" :char-is-proxy="charIsProxy" :errors="errors" v-on="$listeners" />
      </div>

      <!-- Filters -->
      <div class="card">
        <div class="card-header">
          <div class="card-header-title">
            <span>Filters</span>
          </div>
        </div>

        <Filters :minIl="minIl" :maxIl="maxIl" v-on="$listeners" />
      </div>

      <!-- Actions -->
      <div class="card">
        <div class="card-header">
          <div class="card-header-title">
            <span>Actions</span>
          </div>
        </div>

        <Actions :bisList="bisList" :character="character" :char-is-proxy="charIsProxy" :url="url" :method="method" v-on="$listeners" />
      </div>
    </div>

    <div class="column">
      <div class="card">
        <div class="card-header">
          <div class="card-header-title">
            <span>BIS Gear</span>
          </div>
        </div>
        <BIS :bisList="bisList" :errors="errors" :minIl="minIl" :maxIl="maxIl" :displayOffhand="displayOffhand" />
      </div>
    </div>

    <div class="column">
      <div class="card">
        <div class="card-header">
          <div class="card-header-title">
            <span>Current Gear</span>
          </div>
        </div>
        <Current :bisList="bisList" :errors="errors" :minIl="minIl" :maxIl="maxIl" :displayOffhand="displayOffhand" />
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
export default class BISListDesktopForm extends Vue {
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

  // Set up default values for min and max IL, will change as new tiers are released
  @Prop()
  maxIl!: number

  @Prop()
  method!: string

  @Prop()
  minIl!: number

  @Prop()
  url!: string
}
</script>

<style lang="scss">
</style>
