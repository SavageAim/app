<template>
  <div class="field">
    <div class="select is-fullwidth">
      <select :value="value" @input="handleInput" ref="dropdown">
        <option value="na">Select an item type</option>
        <option value="mainhand">Mainhand</option>
        <option value="offhand">Offhand</option>
        <option value="head">Head</option>
        <option value="body">Body</option>
        <option value="hands">Hands</option>
        <option value="legs">Legs</option>
        <option value="feet">Feet</option>
        <option value="earrings">Earrings</option>
        <option value="necklace">Necklace</option>
        <option value="bracelet">Bracelet</option>
        <option value="ring">Ring</option>
        <option value="tome-accessory-augment">Tome Accessory Augment</option>
        <option value="tome-armour-augment">Tome Armour Augment</option>
        <template v-if="displayNonGear">
          <option value="tome-weapon-token">Tome Weapon Token</option>
          <option value="tome-weapon-augment">Tome Weapon Augment</option>
          <option value="mount">Mount</option>
        </template>
      </select>
    </div>
    <p v-if="error !== undefined" class="help is-danger">{{ error[0] }}</p>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'

@Component
export default class ItemDropdown extends Vue {
  @Prop({ default: false })
  displayNonGear!: boolean

  @Prop()
  error!: string[] | undefined

  @Prop()
  value!: number

  get dropdown(): HTMLSelectElement {
    return this.$refs.dropdown as HTMLSelectElement
  }

  handleInput(): void {
    this.$emit('input', this.dropdown.value)
  }
}
</script>

<style lang="scss">
</style>
