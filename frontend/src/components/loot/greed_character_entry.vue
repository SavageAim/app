<template>
  <div class="box list-item" :key="`greed-${entry.member_id}`" data-microtip-position="top" role="tooltip" :aria-label="`BIS Lists: ${entry.greed_lists.length}`" >
    <span class="badge is-info">{{ itemsReceived }}</span>
    <div class="list-data">
      <div class="left">
        {{ entry.character_name }}
      </div>
      <div class="right" v-if="entry.greed_lists.length > 0">
        <div class="tags has-addons is-hidden-touch">
          <span class="tag is-light">
            BIS Lists
          </span>
          <span class="tag is-link">
            {{ entry.greed_lists.length }}
          </span>
        </div>
      </div>
    </div>
    <div v-if="userHasPermission" class="list-actions">
      <button class="button is-success is-loading" v-if="requesting">Give Item</button>
      <button class="button is-success" @click="openCharacter" v-else-if="entry.greed_lists.length > 0">Select BIS</button>
      <button class="button is-success" @click="saveTome" v-else>Give Item</button>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator'
import GreedRaidModal from '@/components/loot/greed_raid_modal.vue'
import GreedTomeModal from '@/components/loot/greed_tome_modal.vue'
import { GreedGear, GreedItem } from '@/interfaces/loot'

@Component
export default class GreedCharacterEntry extends Vue {
  @Prop()
  entry!: GreedGear

  @Prop()
  itemsReceived!: number

  @Prop()
  raid!: boolean

  @Prop()
  requesting!: boolean

  @Prop()
  userHasPermission!: boolean

  saveRaid(list: GreedItem): void {
    this.$emit('save-raid', list)
  }

  saveTome(): void {
    this.$emit('save-tome')
  }

  openCharacter(): void {
    if (this.raid) {
      this.$modal.show(GreedRaidModal, { entry: this.entry, save: this.saveRaid })
    }
    else {
      this.$modal.show(GreedTomeModal, { entry: this.entry, save: this.saveTome })
    }
  }
}
</script>

<style lang="scss">

</style>
