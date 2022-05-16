<template>
  <div class="card-content">
    <GearDropdown :maxIl="maxIl" :minIl="minIl" name="Main Hand" :choices="weapons" v-model="bisList.bis_mainhand_id" :error="errors.bis_mainhand_id" />
    <GearDropdown :maxIl="maxIl" :minIl="minIl" name="Off Hand" :choices="weapons" v-if="displayOffhand" v-model="bisList.bis_offhand_id" :error="errors.bis_offhand_id" />
    <GearDropdown :maxIl="maxIl" :minIl="minIl" name="Head" :choices="armour" v-model="bisList.bis_head_id" :error="errors.bis_head_id" />
    <GearDropdown :maxIl="maxIl" :minIl="minIl" name="Body" :choices="armour" v-model="bisList.bis_body_id" :error="errors.bis_body_id" />
    <GearDropdown :maxIl="maxIl" :minIl="minIl" name="Hands" :choices="armour" v-model="bisList.bis_hands_id" :error="errors.bis_hands_id" />
    <GearDropdown :maxIl="maxIl" :minIl="minIl" name="Legs" :choices="armour" v-model="bisList.bis_legs_id" :error="errors.bis_legs_id" />
    <GearDropdown :maxIl="maxIl" :minIl="minIl" name="Feet" :choices="armour" v-model="bisList.bis_feet_id" :error="errors.bis_feet_id" />
    <GearDropdown :maxIl="maxIl" :minIl="minIl" name="Earrings" :choices="accessories" v-model="bisList.bis_earrings_id" :error="errors.bis_earrings_id" />
    <GearDropdown :maxIl="maxIl" :minIl="minIl" name="Necklace" :choices="accessories" v-model="bisList.bis_necklace_id" :error="errors.bis_necklace_id" />
    <GearDropdown :maxIl="maxIl" :minIl="minIl" name="Bracelet" :choices="accessories" v-model="bisList.bis_bracelet_id" :error="errors.bis_bracelet_id" />
    <GearDropdown :maxIl="maxIl" :minIl="minIl" name="Right Ring" :choices="accessories" v-model="bisList.bis_right_ring_id" :error="errors.bis_right_ring_id" />
    <GearDropdown :maxIl="maxIl" :minIl="minIl" name="Left Ring" :choices="accessories" v-model="bisList.bis_left_ring_id" :error="errors.bis_left_ring_id" />
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'
import GearDropdown from '@/components/gear_dropdown.vue'
import BISListModify from '@/dataclasses/bis_list_modify'
import { BISListErrors } from '@/interfaces/responses'
import Gear from '@/interfaces/gear'

@Component({
  components: {
    GearDropdown,
  },
})
export default class BIS extends Vue {
  @Prop()
  bisList!: BISListModify

  @Prop()
  displayOffhand!: boolean

  @Prop()
  errors!: BISListErrors

  @Prop()
  maxIl!: number

  @Prop()
  minIl!: number

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

  // Filtered array of gear for weapons
  get weapons(): Gear[] {
    return this.gear.filter((item: Gear) => item.has_weapon)
  }
}
</script>

<style lang="scss">
</style>
