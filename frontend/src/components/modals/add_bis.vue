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
      <BISListForm :bisList="bisList" :errors="errors" :render-desktop="false" />
      <button class="button is-fullwidth is-success" @click="save">Add</button>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'
import BISListForm from '@/components/bis_list_form.vue'
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

  // Save the data into a new bis list
  async save(): Promise<void> {
    const body = JSON.stringify(this.bisList)
    try {
      const response = await fetch(this.url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': this.$cookies.get('csrftoken'),
        },
        body,
      })

      if (response.ok) {
        // Redirect back to the new bis list page
        this.$notify({ text: `New BIS List created successfully! It should appear in your BIS dropdown now!`, type: 'is-success' })
        this.$emit('close')
      }
      else {
        this.errors = (await response.json() as BISListErrors)
      }
    }
    catch (e) {
      this.$notify({ text: `Error ${e} when attempting to create BIS List.`, type: 'is-danger' })
    }
  }
}
</script>

<style lang="scss">
</style>
