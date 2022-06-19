<template>
  <div>
    <label class="checkbox" :disabled="!enabled">
      <input type="checkbox" :disabled="!enabled" :checked="value" @input="handleInput" ref="checkbox" />
      <span :class="{'is-sr-only': !displayLabel}">{{ label }}</span>
    </label>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'

@Component
export default class PermissionInput extends Vue {
  @Prop({ default: true })
  displayLabel!: boolean

  @Prop({ default: true })
  enabled!: boolean

  @Prop()
  label!: string

  @Prop()
  value!: boolean

  get checkbox(): HTMLInputElement {
    return this.$refs.checkbox as HTMLInputElement
  }

  handleInput(): void {
    this.$emit('input', this.checkbox.checked)
  }
}
</script>

<style lang="scss">
.checkbox span {
  margin-left: 0.2rem;
}
</style>
