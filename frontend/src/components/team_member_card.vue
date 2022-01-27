<template>
  <div class="column is-half-desktop">
    <div class="card">
      <div class="card-header">
        <div class="card-header-title">
          <span class="icon-text">
            <span class="icon is-hidden-touch" v-if="details.lead"><img src="/party_lead.png" alt="Team Lead" title="Team Lead" /></span>
            <span class="icon is-hidden-touch" v-else><img src="/party_member.png" alt="Team Member" title="Team Member" /></span>
            <span>{{ details.character.name }} @ {{ details.character.world }}</span>
          </span>
        </div>
        <div class="card-header-icon">
          <div class="tags has-addons is-hidden-touch">
            <span class="tag is-light">
              iL
            </span>
            <span class="tag" :class="[`is-${details.bis_list.job.role}`]">
              {{ details.bis_list.item_level }}
            </span>
          </div>
          <span class="icon">
            <img :src="`/job_icons/${details.bis_list.job.name}.png`" :alt="`${details.bis_list.job.name} job icon`" />
          </span>
        </div>
      </div>
      <div class="card-content">
        <table class="table is-bordered is-fullwidth is-hidden-touch gear-table" :class="[`is-${$store.state.user.theme}`]">
          <tbody>
            <tr>
              <template v-if="details.bis_list.job.name === 'paladin'">
                <th>Weapon</th>
                <td data-microtip-position="top" role="tooltip" :aria-label="`Current: ${details.bis_list.current_mainhand.name}`" :class="[getColourClass(details.bis_list.current_mainhand, details.bis_list.bis_mainhand)]">{{ details.bis_list.bis_mainhand.name }}</td>

                <th>Shield</th>
                <td data-microtip-position="top" role="tooltip" :aria-label="`Current: ${details.bis_list.current_offhand.name}`" :class="[getColourClass(details.bis_list.current_offhand, details.bis_list.bis_offhand)]">{{ details.bis_list.bis_offhand.name }}</td>
              </template>

              <template v-else>
                <th colspan="2">Weapon</th>
                <td colspan="2" data-microtip-position="top" role="tooltip" :aria-label="`Current: ${details.bis_list.current_mainhand.name}`" :class="[getColourClass(details.bis_list.current_mainhand, details.bis_list.bis_mainhand)]">{{ details.bis_list.bis_mainhand.name }}</td>
              </template>
            </tr>
            <tr>
              <th>Head</th>
              <td data-microtip-position="top" role="tooltip" :aria-label="`Current: ${details.bis_list.current_head.name}`" :class="[getColourClass(details.bis_list.current_head, details.bis_list.bis_head)]">{{ details.bis_list.bis_head.name }}</td>
              <th>Earrings</th>
              <td data-microtip-position="top" role="tooltip" :aria-label="`Current: ${details.bis_list.current_earrings.name}`" :class="[getColourClass(details.bis_list.current_earrings, details.bis_list.bis_earrings)]">{{ details.bis_list.bis_earrings.name }}</td>
            </tr>
            <tr>
              <th>Body</th>
              <td data-microtip-position="top" role="tooltip" :aria-label="`Current: ${details.bis_list.current_body.name}`" :class="[getColourClass(details.bis_list.current_body, details.bis_list.bis_body)]">{{ details.bis_list.bis_body.name }}</td>
              <th>Necklace</th>
              <td data-microtip-position="top" role="tooltip" :aria-label="`Current: ${details.bis_list.current_necklace.name}`" :class="[getColourClass(details.bis_list.current_necklace, details.bis_list.bis_necklace)]">{{ details.bis_list.bis_necklace.name }}</td>
            </tr>
            <tr>
              <th>Hands</th>
              <td data-microtip-position="top" role="tooltip" :aria-label="`Current: ${details.bis_list.current_hands.name}`" :class="[getColourClass(details.bis_list.current_hands, details.bis_list.bis_hands)]">{{ details.bis_list.bis_hands.name }}</td>
              <th>Bracelet</th>
              <td data-microtip-position="top" role="tooltip" :aria-label="`Current: ${details.bis_list.current_bracelet.name}`" :class="[getColourClass(details.bis_list.current_bracelet, details.bis_list.bis_bracelet)]">{{ details.bis_list.bis_bracelet.name }}</td>
            </tr>
            <tr>
              <th>Legs</th>
              <td data-microtip-position="top" role="tooltip" :aria-label="`Current: ${details.bis_list.current_legs.name}`" :class="[getColourClass(details.bis_list.current_legs, details.bis_list.bis_legs)]">{{ details.bis_list.bis_legs.name }}</td>
              <th>Right Ring</th>
              <td data-microtip-position="top" role="tooltip" :aria-label="`Current: ${details.bis_list.current_right_ring.name}`" :class="[getColourClass(details.bis_list.current_right_ring, details.bis_list.bis_right_ring)]">{{ details.bis_list.bis_right_ring.name }}</td>
            </tr>
            <tr>
              <th>Feet</th>
              <td data-microtip-position="top" role="tooltip" :aria-label="`Current: ${details.bis_list.current_feet.name}`" :class="[getColourClass(details.bis_list.current_feet, details.bis_list.bis_feet)]">{{ details.bis_list.bis_feet.name }}</td>
              <th>Left Ring</th>
              <td data-microtip-position="top" role="tooltip" :aria-label="`Current: ${details.bis_list.current_left_ring.name}`" :class="[getColourClass(details.bis_list.current_left_ring, details.bis_list.bis_left_ring)]">{{ details.bis_list.bis_left_ring.name }}</td>
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
                    <td data-microtip-position="top" role="tooltip" :aria-label="`Current: ${details.bis_list.current_mainhand.name}`" :class="[getColourClass(details.bis_list.current_mainhand, details.bis_list.bis_mainhand)]">{{ details.bis_list.bis_mainhand.name }}</td>
                  </tr>
                  <tr>
                    <th>Head</th>
                    <td data-microtip-position="top" role="tooltip" :aria-label="`Current: ${details.bis_list.current_head.name}`" :class="[getColourClass(details.bis_list.current_head, details.bis_list.bis_head)]">{{ details.bis_list.bis_head.name }}</td>
                  </tr>
                  <tr>
                    <th>Body</th>
                    <td data-microtip-position="top" role="tooltip" :aria-label="`Current: ${details.bis_list.current_body.name}`" :class="[getColourClass(details.bis_list.current_body, details.bis_list.bis_body)]">{{ details.bis_list.bis_body.name }}</td>
                  </tr>
                  <tr>
                    <th>Hands</th>
                    <td data-microtip-position="top" role="tooltip" :aria-label="`Current: ${details.bis_list.current_hands.name}`" :class="[getColourClass(details.bis_list.current_hands, details.bis_list.bis_hands)]">{{ details.bis_list.bis_hands.name }}</td>
                  </tr>
                  <tr>
                    <th>Legs</th>
                    <td data-microtip-position="top" role="tooltip" :aria-label="`Current: ${details.bis_list.current_legs.name}`" :class="[getColourClass(details.bis_list.current_legs, details.bis_list.bis_legs)]">{{ details.bis_list.bis_legs.name }}</td>
                  </tr>
                  <tr>
                    <th>Feet</th>
                    <td data-microtip-position="top" role="tooltip" :aria-label="`Current: ${details.bis_list.current_feet.name}`" :class="[getColourClass(details.bis_list.current_feet, details.bis_list.bis_feet)]">{{ details.bis_list.bis_feet.name }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div ref="rhs" class="is-hidden">
              <table class="table is-bordered is-fullwidth gear-table" :class="[`is-${$store.state.user.theme}`]">
                <tbody>
                  <tr>
                    <template v-if="details.bis_list.job === 'paladin'">
                      <th>Shield</th>
                      <td data-microtip-position="top" role="tooltip" :aria-label="`Current: ${details.bis_list.current_offhand.name}`" :class="[getColourClass(details.bis_list.current_offhand, details.bis_list.bis_offhand)]">{{ details.bis_list.bis_offhand.name }}</td>
                    </template>
                  </tr>
                  <tr>
                    <th>Earrings</th>
                    <td data-microtip-position="top" role="tooltip" :aria-label="`Current: ${details.bis_list.current_earrings.name}`" :class="[getColourClass(details.bis_list.current_earrings, details.bis_list.bis_earrings)]">{{ details.bis_list.bis_earrings.name }}</td>
                  </tr>
                  <tr>
                    <th>Necklace</th>
                    <td data-microtip-position="top" role="tooltip" :aria-label="`Current: ${details.bis_list.current_necklace.name}`" :class="[getColourClass(details.bis_list.current_necklace, details.bis_list.bis_necklace)]">{{ details.bis_list.bis_necklace.name }}</td>
                  </tr>
                  <tr>
                    <th>Bracelet</th>
                    <td data-microtip-position="top" role="tooltip" :aria-label="`Current: ${details.bis_list.current_bracelet.name}`" :class="[getColourClass(details.bis_list.current_bracelet, details.bis_list.bis_bracelet)]">{{ details.bis_list.bis_bracelet.name }}</td>
                  </tr>
                  <tr>
                    <th>Right Ring</th>
                    <td data-microtip-position="top" role="tooltip" :aria-label="`Current: ${details.bis_list.current_right_ring.name}`" :class="[getColourClass(details.bis_list.current_right_ring, details.bis_list.bis_right_ring)]">{{ details.bis_list.bis_right_ring.name }}</td>
                  </tr>
                  <tr>
                    <th>Left Ring</th>
                    <td data-microtip-position="top" role="tooltip" :aria-label="`Current: ${details.bis_list.current_left_ring.name}`" :class="[getColourClass(details.bis_list.current_left_ring, details.bis_list.bis_left_ring)]">{{ details.bis_list.bis_left_ring.name }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
      <footer class="card-footer">
        <a v-if="details.bis_list.external_link != null" target="_blank" :href="details.bis_list.external_link" class="card-footer-item">
          View on {{ details.bis_list.external_link.replace(/https?:\/\//, '').split('/')[0] }}
        </a>
        <template v-if="owner">
          <!-- Quick link to edit this bis list -->
          <router-link :to="`/characters/${details.character.id}/bis_list/${details.bis_list.id}/`" class="card-footer-item">
            Edit List
          </router-link>
          <!-- Link to update the TeamMember details with new character / bislist -->
          <router-link :to="`./member/${details.id}/`" class="card-footer-item">
            Change Character
          </router-link>
          <!-- Modal to confirm, leave team -->
          <!-- <a class="card-footer-item" v-if="!details.lead">
            Leave Team
          </a> -->
        </template>
        <!-- Admin Commands -->
        <!-- <template v-if="!owner && editable">
          Modal to confirm, kick from team
          <a class="card-footer-item">
            Kick from Team
          </a>
        </template> -->
      </footer>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator'
import Gear from '@/interfaces/gear'
import TeamMember from '@/interfaces/team_member'

@Component
export default class TeamMemberCard extends Vue {
  // Allows rendering other team member's cards with the kick button below
  @Prop()
  editable!: boolean

  @Prop()
  details!: TeamMember

  @Prop()
  maxItemLevel!: number

  private leftShown = false

  private rightShown = false

  get lhs(): Element {
    return this.$refs.lhs as Element
  }

  get rhs(): Element {
    return this.$refs.rhs as Element
  }

  get lhsTab(): Element {
    return this.$refs.lhsTab as Element
  }

  get rhsTab(): Element {
    return this.$refs.rhsTab as Element
  }

  // Flag stating whether the logged in user is the owner of the member on this card
  get owner(): boolean {
    return this.$store.state.user.id === this.details.character.user_id
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
</style>
