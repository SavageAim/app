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
      <button class="button is-success" @click="saveWithoutUpdate" v-else>Give Item</button>
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
  item!: string

  @Prop()
  itemsReceived!: number

  @Prop()
  requesting!: boolean

  @Prop()
  userHasPermission!: boolean

  save(list: GreedItem): void {
    // A main level function to determine how we save. The modal type can no longer make the determination for us
    // Some items cannot be saved with an update, even if they are displayed using the raid modal
    if (this.item.indexOf('tome') !== -1 || this.item === 'mount') {
      // We cannot run an update but we do want to save them
      this.saveWithoutUpdate()
    }
    else {
      // Anything else can be updated since it's all raid gear
      this.saveWithUpdate(list)
    }
  }

  saveWithUpdate(list: GreedItem): void {
    this.$emit('save-with-update', list)
  }

  saveWithoutUpdate(): void {
    this.$emit('save-without-update')
  }

  openCharacter(): void {
    // Pick the modal to display. "RaidModal" displays current_item_il, "TomeModal" displays a number of required tokens.
    // We'll be using Raid unless the item is tome-accessory-augment or tome-armour-augment
    if (this.item === 'tome-accessory-augment' || this.item === 'tome-armour-augment') {
      // Display the modal that shows requires
      this.$modal.show(GreedTomeModal, { entry: this.entry, save: this.save })
    }
    else {
      // Display the modal that shows item levels
      this.$modal.show(GreedRaidModal, { entry: this.entry, save: this.save })
    }
  }
}
</script>

<style lang="scss">

</style>
