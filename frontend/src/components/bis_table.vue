<template>
  <div>
    <table class="table is-bordered is-fullwidth is-hidden-touch gear-table" :class="[`is-${$store.state.user.theme}`]">
      <tbody>
        <tr>
          <template v-if="list.job.name === 'paladin'">
            <th>Weapon</th>
            <td data-microtip-position="top" role="tooltip" :aria-label="`Current: ${list.current_mainhand.name}`" :class="[getColourClass(list.current_mainhand, list.bis_mainhand)]">{{ list.bis_mainhand.name }}</td>

            <th>Shield</th>
            <td data-microtip-position="top" role="tooltip" :aria-label="`Current: ${list.current_offhand.name}`" :class="[getColourClass(list.current_offhand, list.bis_offhand)]">{{ list.bis_offhand.name }}</td>
          </template>

          <template v-else>
            <th colspan="2">Weapon</th>
            <td colspan="2" data-microtip-position="top" role="tooltip" :aria-label="`Current: ${list.current_mainhand.name}`" :class="[getColourClass(list.current_mainhand, list.bis_mainhand)]">{{ list.bis_mainhand.name }}</td>
          </template>
        </tr>
        <tr>
          <th>Head</th>
          <td data-microtip-position="top" role="tooltip" :aria-label="`Current: ${list.current_head.name}`" :class="[getColourClass(list.current_head, list.bis_head)]">{{ list.bis_head.name }}</td>
          <th>Earrings</th>
          <td data-microtip-position="top" role="tooltip" :aria-label="`Current: ${list.current_earrings.name}`" :class="[getColourClass(list.current_earrings, list.bis_earrings)]">{{ list.bis_earrings.name }}</td>
        </tr>
        <tr>
          <th>Body</th>
          <td data-microtip-position="top" role="tooltip" :aria-label="`Current: ${list.current_body.name}`" :class="[getColourClass(list.current_body, list.bis_body)]">{{ list.bis_body.name }}</td>
          <th>Necklace</th>
          <td data-microtip-position="top" role="tooltip" :aria-label="`Current: ${list.current_necklace.name}`" :class="[getColourClass(list.current_necklace, list.bis_necklace)]">{{ list.bis_necklace.name }}</td>
        </tr>
        <tr>
          <th>Hands</th>
          <td data-microtip-position="top" role="tooltip" :aria-label="`Current: ${list.current_hands.name}`" :class="[getColourClass(list.current_hands, list.bis_hands)]">{{ list.bis_hands.name }}</td>
          <th>Bracelet</th>
          <td data-microtip-position="top" role="tooltip" :aria-label="`Current: ${list.current_bracelet.name}`" :class="[getColourClass(list.current_bracelet, list.bis_bracelet)]">{{ list.bis_bracelet.name }}</td>
        </tr>
        <tr>
          <th>Legs</th>
          <td data-microtip-position="top" role="tooltip" :aria-label="`Current: ${list.current_legs.name}`" :class="[getColourClass(list.current_legs, list.bis_legs)]">{{ list.bis_legs.name }}</td>
          <th>Right Ring</th>
          <td data-microtip-position="top" role="tooltip" :aria-label="`Current: ${list.current_right_ring.name}`" :class="[getColourClass(list.current_right_ring, list.bis_right_ring)]">{{ list.bis_right_ring.name }}</td>
        </tr>
        <tr>
          <th>Feet</th>
          <td data-microtip-position="top" role="tooltip" :aria-label="`Current: ${list.current_feet.name}`" :class="[getColourClass(list.current_feet, list.bis_feet)]">{{ list.bis_feet.name }}</td>
          <th>Left Ring</th>
          <td data-microtip-position="top" role="tooltip" :aria-label="`Current: ${list.current_left_ring.name}`" :class="[getColourClass(list.current_left_ring, list.bis_left_ring)]">{{ list.bis_left_ring.name }}</td>
        </tr>
      </tbody>
    </table>

    <!-- Mobile View -->
    <div class="is-hidden-desktop">
      <div class="tabs is-centered is-boxed is-fullwidth">
        <ul>
          <li ref="lhsTab" @click="toggleLeft"><a>Left Side</a></li>
          <li ref="rhsTab" @click="toggleRight"><a>Right Side</a></li>
        </ul>
      </div>
      <div class="tab-content">
        <div ref="lhs" class="is-hidden">
          <table class="table is-bordered is-fullwidth gear-table" :class="[`is-${$store.state.user.theme}`]">
            <tbody>
              <tr>
                <th>Weapon</th>
                <td data-microtip-position="top" role="tooltip" :aria-label="`Current: ${list.current_mainhand.name}`" :class="[getColourClass(list.current_mainhand, list.bis_mainhand)]">{{ list.bis_mainhand.name }}</td>
              </tr>
              <tr>
                <th>Head</th>
                <td data-microtip-position="top" role="tooltip" :aria-label="`Current: ${list.current_head.name}`" :class="[getColourClass(list.current_head, list.bis_head)]">{{ list.bis_head.name }}</td>
              </tr>
              <tr>
                <th>Body</th>
                <td data-microtip-position="top" role="tooltip" :aria-label="`Current: ${list.current_body.name}`" :class="[getColourClass(list.current_body, list.bis_body)]">{{ list.bis_body.name }}</td>
              </tr>
              <tr>
                <th>Hands</th>
                <td data-microtip-position="top" role="tooltip" :aria-label="`Current: ${list.current_hands.name}`" :class="[getColourClass(list.current_hands, list.bis_hands)]">{{ list.bis_hands.name }}</td>
              </tr>
              <tr>
                <th>Legs</th>
                <td data-microtip-position="top" role="tooltip" :aria-label="`Current: ${list.current_legs.name}`" :class="[getColourClass(list.current_legs, list.bis_legs)]">{{ list.bis_legs.name }}</td>
              </tr>
              <tr>
                <th>Feet</th>
                <td data-microtip-position="top" role="tooltip" :aria-label="`Current: ${list.current_feet.name}`" :class="[getColourClass(list.current_feet, list.bis_feet)]">{{ list.bis_feet.name }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        <div ref="rhs" class="is-hidden">
          <table class="table is-bordered is-fullwidth gear-table" :class="[`is-${$store.state.user.theme}`]">
            <tbody>
              <tr>
                <template v-if="list.job.name === 'paladin'">
                  <th>Shield</th>
                  <td data-microtip-position="top" role="tooltip" :aria-label="`Current: ${list.current_offhand.name}`" :class="[getColourClass(list.current_offhand, list.bis_offhand)]">{{ list.bis_offhand.name }}</td>
                </template>
              </tr>
              <tr>
                <th>Earrings</th>
                <td data-microtip-position="top" role="tooltip" :aria-label="`Current: ${list.current_earrings.name}`" :class="[getColourClass(list.current_earrings, list.bis_earrings)]">{{ list.bis_earrings.name }}</td>
              </tr>
              <tr>
                <th>Necklace</th>
                <td data-microtip-position="top" role="tooltip" :aria-label="`Current: ${list.current_necklace.name}`" :class="[getColourClass(list.current_necklace, list.bis_necklace)]">{{ list.bis_necklace.name }}</td>
              </tr>
              <tr>
                <th>Bracelet</th>
                <td data-microtip-position="top" role="tooltip" :aria-label="`Current: ${list.current_bracelet.name}`" :class="[getColourClass(list.current_bracelet, list.bis_bracelet)]">{{ list.bis_bracelet.name }}</td>
              </tr>
              <tr>
                <th>Right Ring</th>
                <td data-microtip-position="top" role="tooltip" :aria-label="`Current: ${list.current_right_ring.name}`" :class="[getColourClass(list.current_right_ring, list.bis_right_ring)]">{{ list.bis_right_ring.name }}</td>
              </tr>
              <tr>
                <th>Left Ring</th>
                <td data-microtip-position="top" role="tooltip" :aria-label="`Current: ${list.current_left_ring.name}`" :class="[getColourClass(list.current_left_ring, list.bis_left_ring)]">{{ list.bis_left_ring.name }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator'
import BISList from '@/interfaces/bis_list'
import Gear from '@/interfaces/gear'

@Component
export default class BISTable extends Vue {
  // Allows rendering other team member's cards with the kick button below
  @Prop({ default: null })
  itemLevel!: number | null

  @Prop()
  list!: BISList

  private leftShown = false

  private rightShown = false

  get maxItemLevel(): number {
    if (this.itemLevel !== null) return this.itemLevel
    // Use bis mainhand item level, since we can assume this will *probably* be the raid weapon
    return this.list.bis_mainhand.item_level
  }

  get lhs(): Element {
    return this.$refs.lhs as Element
  }

  get lhsTab(): Element {
    return this.$refs.lhsTab as Element
  }

  get rhs(): Element {
    return this.$refs.rhs as Element
  }

  get rhsTab(): Element {
    return this.$refs.rhsTab as Element
  }

  // Method to get css class for the item given
  getColourClass(current: Gear, bis: Gear): string {
    if (current.id === bis.id) return 'is-il-bis'
    if (current.item_level > this.maxItemLevel || current.item_level < this.maxItemLevel - 25) return 'is-il-out-of-range'
    return `is-il-minus-${this.maxItemLevel - current.item_level}`
  }

  // Tab toggling methods
  toggleLeft(): void {
    this.hideTabs()
    this.rightShown = false
    if (!this.leftShown) {
      this.lhs.classList.remove('is-hidden')
      this.lhsTab.classList.add('is-active')
      this.leftShown = true
    }
    else {
      this.leftShown = false
    }
  }

  toggleRight(): void {
    this.hideTabs()
    this.leftShown = false
    if (!this.rightShown) {
      this.rhs.classList.remove('is-hidden')
      this.rhsTab.classList.add('is-active')
      this.rightShown = true
    }
    else {
      this.rightShown = false
    }
  }

  hideTabs(): void {
    this.lhs.classList.add('is-hidden')
    this.rhs.classList.add('is-hidden')
    this.lhsTab.classList.remove('is-active')
    this.rhsTab.classList.remove('is-active')
  }
}
</script>

<style lang="scss">
td[role=tooltip] {
  background-clip: padding-box;
}
table.gear-table:not(:last-child) {
  margin-bottom: 0;
}
</style>
