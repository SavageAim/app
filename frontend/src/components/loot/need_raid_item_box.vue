<template>
  <div class="box list-item" :key="`need-${entry.member_id}`" data-microtip-position="top" role="tooltip" :aria-label="`Current: ${entry.current_gear_name}`" >
    <span class="badge is-primary">{{ itemsReceived }}</span>
    <div class="list-data">
      <div class="left">
        {{ entry.character_name }}
      </div>
      <div class="right">
        <div class="tags has-addons is-hidden-touch">
          <span class="tag is-light">
            iL
          </span>
          <span class="tag" :class="[`is-${entry.job_role}`]">
            {{ entry.current_gear_il }}
          </span>
        </div>
        <span class="icon">
          <img :src="`/job_icons/${entry.job_icon_name}.png`" :alt="`${entry.job_icon_name} job icon`" />
        </span>
      </div>
    </div>
    <div v-if="editable" class="list-actions">
      <button class="button is-success" @click="save" v-if="!requesting">Give Item</button>
      <button class="button is-success is-loading" v-else>Give Item</button>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator'
import { NeedGear } from '@/interfaces/loot'

@Component
export default class NeedRaidItem extends Vue {
  @Prop()
  editable!: boolean

  @Prop()
  entry!: NeedGear

  @Prop()
  itemsReceived!: number

  @Prop()
  requesting!: boolean

  save(): void {
    this.$emit('save')
  }
}
</script>

<style lang="scss">

</style>
