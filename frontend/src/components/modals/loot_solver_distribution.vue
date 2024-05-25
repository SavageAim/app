<template>
  <div>
    <div class="card-header">
      <div class="card-header-title">
        Loot Distribution for {{ fight }}
      </div>
      <div class="card-header-icon">
        <a class="icon" @click="() => { this.$emit('close') }">
          <i class="material-icons">close</i>
        </a>
      </div>
    </div>
    <div class="card-content">
      <table class="table is-fullwidth is-striped is-bordered">
        <thead>
          <tr>
            <th>Kill</th>
            <th v-for="header in headers" :key="header">{{ header }}</th>
          </tr>
        </thead>
        <tbody>
          <template v-for="(kill, index) in data">
            <tr :key="index">
              <th>#{{ index + 1 }}</th>
              <template v-for="header in headers">
                <td :key="`kill-${index+1}-item-${header}`" v-if="teamMemberNames[kill[header]]">{{ teamMemberNames[kill[header]] }}</td>
                <td :key="`kill-${index+1}-item-${header}`" v-else class="has-text-info">Greed</td>
              </template>
            </tr>
            <tr :key="`token-${index}`" v-if="kill.token">
              <th :colspan="headers.length + 1">Token Purchase</th>
            </tr>
          </template>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'

@Component
export default class LootSolverDistributionTable extends Vue {
  @Prop()
  data!: { [item: string]: number }[]

  @Prop()
  fight!: string

  @Prop()
  teamMemberNames!: { [id: number]: string }

  get headers(): string[] {
    // Can't display the Modal if data.length == 0 so this is safe
    const dataKeys = Object.keys(this.data[0])
    if (dataKeys.includes('Earrings')) return ['Earrings', 'Necklace', 'Bracelet', 'Ring']
    if (dataKeys.includes('Head')) return ['Head', 'Hands', 'Feet', 'Tome Accessory Augment']
    return ['Body', 'Legs', 'Tome Armour Augment']
  }
}
</script>

<style lang="scss">
</style>
