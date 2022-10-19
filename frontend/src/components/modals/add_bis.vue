<template>
  <div>
    <div class="card-header">
      <div class="card-header-title">
        {{ character.name }} @ {{ character.world }} - Add BIS
      </div>
      <div class="card-header-icon">
        <a class="icon" @click="() => { this.$emit('close') }">
          <i class="material-icons">close</i>
        </a>
      </div>
    </div>
    <div class="card-content">
      <BISListForm :bisList="bisList" :character="character" :url="url" method="POST" v-on:error-code="handleError" :render-desktop="false" v-on:close="$emit('close')" />
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'
import BISListForm from '@/components/bis_list/form.vue'
import BISListModify from '@/dataclasses/bis_list_modify'
import { CharacterDetails } from '@/interfaces/character'
import { BISListErrors } from '@/interfaces/responses'

@Component({
  components: {
    BISListForm,
  },
})
export default class AddBIS extends Vue {
  bisList = new BISListModify()

  @Prop()
  character!: CharacterDetails

  errors: BISListErrors = {}

  // Url to send data to
  get url(): string {
    return `/backend/api/character/${this.character.id}/bis_lists/`
  }

  handleError(errorCode: number): void {
    if (errorCode === 400) return
    this.$notify({ text: `Something went wrong; HTTP ${errorCode}. Try adding a new BIS from the standard page instead.`, type: 'is-danger' })
  }
}
</script>

<style lang="scss">
</style>
