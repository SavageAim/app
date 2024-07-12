<template>
  <div>
    <div class="card-header">
      <div class="card-header-title">Select a set to import from XIVGear.</div>
      <div class="card-header-icon">
        <a class="icon" @click="() => { this.$emit('close') }">
          <i class="material-icons">close</i>
        </a>
      </div>
    </div>
    <div class="card-content">
      <p>Multiple gearsets were found in your provided XIVGear link. Please select one of the following to import!</p>
      <hr />
      <a class="box" v-for="sheet in sheets" :key="sheet.index" @click="() => { importSet(sheet.index) }">
        <p>{{ sheet.name }}</p>
      </a>
    </div>
    <footer class="card-footer">
      <a class="card-footer-item has-text-link" @click="() => { this.$emit('close') }">
        <span class="icon-text">
          <span class="icon"><i class="material-icons">close</i></span>
          <span>Cancel</span>
        </span>
      </a>
    </footer>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'
import { XIVGearSheetSelection } from '@/interfaces/imports'

@Component
export default class XIVGearSheetSetSelection extends Vue {
  @Prop()
  doImport!: (setNum: number) => Promise<void>

  @Prop()
  sheets!: XIVGearSheetSelection[]

  importSet(setNum: number) {
    this.doImport(setNum)
    this.$emit('close')
  }
}
</script>
