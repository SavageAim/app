<template>
  <div class="card-content">
    <GearDropdown :maxIl="maxIl" :minIl="minIl" name="Main Hand" :choices="weapons" v-model="bisList.current_mainhand_id" :error="errors.current_mainhand_id" :bisValue="bisList.bis_mainhand_id" />
    <GearDropdown :maxIl="maxIl" :minIl="minIl" name="Off Hand" :choices="weapons" v-if="displayOffhand" v-model="bisList.current_offhand_id" :error="errors.current_offhand_id" :bisValue="bisList.bis_offhand_id" />
    <GearDropdown :maxIl="maxIl" :minIl="minIl" name="Head" :choices="armour" v-model="bisList.current_head_id" :error="errors.current_head_id" :bisValue="bisList.bis_head_id" />
    <GearDropdown :maxIl="maxIl" :minIl="minIl" name="Body" :choices="armour" v-model="bisList.current_body_id" :error="errors.current_body_id" :bisValue="bisList.bis_body_id" />
    <GearDropdown :maxIl="maxIl" :minIl="minIl" name="Hands" :choices="armour" v-model="bisList.current_hands_id" :error="errors.current_hands_id" :bisValue="bisList.bis_hands_id" />
    <GearDropdown :maxIl="maxIl" :minIl="minIl" name="Legs" :choices="armour" v-model="bisList.current_legs_id" :error="errors.current_legs_id" :bisValue=bisList.bis_legs_id />
    <GearDropdown :maxIl="maxIl" :minIl="minIl" name="Feet" :choices="armour" v-model="bisList.current_feet_id" :error="errors.current_feet_id" :bisValue="bisList.bis_feet_id" />
    <GearDropdown :maxIl="maxIl" :minIl="minIl" name="Earrings" :choices="accessories" v-model="bisList.current_earrings_id" :error="errors.current_earrings_id" :bisValue="bisList.bis_earrings_id" />
    <GearDropdown :maxIl="maxIl" :minIl="minIl" name="Necklace" :choices="accessories" v-model="bisList.current_necklace_id" :error="errors.current_necklace_id" :bisValue="bisList.bis_necklace_id" />
    <GearDropdown :maxIl="maxIl" :minIl="minIl" name="Bracelet" :choices="accessories" v-model="bisList.current_bracelet_id" :error="errors.current_bracelet_id" :bisValue="bisList.bis_bracelet_id" />
    <GearDropdown :maxIl="maxIl" :minIl="minIl" name="Right Ring" :choices="accessories" v-model="bisList.current_right_ring_id" :error="errors.current_right_ring_id" :bisValue="bisList.bis_right_ring_id" />
    <GearDropdown :maxIl="maxIl" :minIl="minIl" name="Left Ring" :choices="accessories" v-model="bisList.current_left_ring_id" :error="errors.current_left_ring_id" :bisValue="bisList.bis_left_ring_id" />
  </div>
</template>

<script lang="ts">
import { Component } from 'vue-property-decorator'
import GearDropdown from '@/components/gear_dropdown.vue'
import BIS from '@/components/bis_list/bis.vue'

@Component({
  components: {
    GearDropdown,
  },
})
export default class Current extends BIS {}
</script>

<style lang="scss">
</style>
