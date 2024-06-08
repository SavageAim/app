<template>
  <div>
    <div class="card">
      <div class="card-header">
        <div class="card-header-title">User Details</div>
      </div>
      <div class="card-content">
        <div class="field is-horizontal">
          <div class="field-label is-normal">
            <label class="label">Username</label>
          </div>
          <div class="field-body">
            <div class="field">
              <div class="control">
                <input class="input" :class="{'is-danger': errors.username !== undefined}" :value="username" ref="input" @input="changeUsername" />
              </div>
              <p v-if="errors.username !== undefined" class="help is-danger">{{ errors.username[0] }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="card">
      <div class="card-header">
        <div class="card-header-title">API Key</div>
      </div>
      <div class="card-content">
        <button v-if="token === null" class="button is-success is-fullwidth" @click="getToken">Generate an API Key!</button>
        <div class="field has-addons" v-else>
          <div class="control is-expanded">
            <input class="input is-dark" id="apiKey" type="text" :value="token" readonly />
            <p class="help">Use an API Key to access the site from other places!</p>
          </div>
          <label class="label is-sr-only" for="inviteCode">Savage Aim API Key</label>
          <div class="control">
            <button class="button is-dark" @click="getToken">Regenerate Key</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'
import { SettingsErrors } from '@/interfaces/responses'

@Component
export default class UserDetailsSettings extends Vue {
  @Prop()
  errors!: SettingsErrors

  @Prop()
  token!: string | null

  @Prop()
  username!: string

  get input(): HTMLInputElement {
    return this.$refs.input as HTMLInputElement
  }

  changeUsername(): void {
    this.$emit('changeUsername', this.input.value)
  }

  async getToken(): Promise<void> {
    console.log('getToken')
  }
}
</script>
