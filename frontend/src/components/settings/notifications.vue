<template>
  <div class="card">
    <div class="card-header">
      <div class="card-header-title">Notifications</div>
    </div>
    <div class="card-content">
      <p class="has-text-info">
        Tick or untick boxes for the Notifications you do / don't want to receive!
        <br />Please note this only affects future notifications and will not delete any existing ones.
      </p>
      <div class="divider"><i class="material-icons icon">expand_more</i> Character <i class="material-icons icon">expand_more</i></div>
      <div class="field">
        <label class="checkbox">
          <input type="checkbox" :checked="notifications.verify_success" data-name="verify_success" @input="changeNotification">
          Character Verification was successful.
        </label>
      </div>
      <div class="field">
        <label class="checkbox">
          <input type="checkbox" :checked="notifications.verify_fail" data-name="verify_fail" @input="changeNotification">
          Character Verification failed.
        </label>
      </div>

      <div class="divider"><i class="material-icons icon">expand_more</i> Team <i class="material-icons icon">expand_more</i></div>
      <div class="field">
        <label class="checkbox">
          <input type="checkbox" :checked="notifications.team_disband" data-name="team_disband" @input="changeNotification">
          A Team that one of your Characters was in has been disbanded.
        </label>
      </div>
      <div class="field">
        <label class="checkbox">
          <input type="checkbox" :checked="notifications.team_join" data-name="team_join" @input="changeNotification">
          A Character has joined one of the Teams you lead.
        </label>
      </div>
      <div class="field">
        <label class="checkbox">
          <input type="checkbox" :checked="notifications.team_kick" data-name="team_kick" @input="changeNotification">
          A Character has been kicked from a Team.
        </label>
      </div>
      <div class="field">
        <label class="checkbox">
          <input type="checkbox" :checked="notifications.team_lead" data-name="team_lead" @input="changeNotification">
          Your Character has been made leader of a Team.
        </label>
      </div>
      <div class="field">
        <label class="checkbox">
          <input type="checkbox" :checked="notifications.team_leave" data-name="team_leave" @input="changeNotification">
          A Character has left one of the Teams you lead.
        </label>
      </div>
      <div class="field">
        <label class="checkbox">
          <input type="checkbox" :checked="notifications.team_proxy_claim" data-name="team_proxy_claim" @input="changeNotification">
          A Proxy Character in one of your Teams has been claimed by a user.
        </label>
      </div>
      <div class="field">
        <label class="checkbox">
          <input type="checkbox" :checked="notifications.team_rename" data-name="team_rename" @input="changeNotification">
          A Team that one of your Characters is in has been renamed.
        </label>
      </div>

      <div class="divider"><i class="material-icons icon">expand_more</i> Loot Manager <i class="material-icons icon">expand_more</i></div>
      <div class="field">
        <label class="checkbox">
          <input type="checkbox" :checked="notifications.loot_tracker_update" data-name="loot_tracker_update" @input="changeNotification">
          Loot Tracker updates your BIS List.
        </label>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'
import NotificationSettings from '@/interfaces/notification_settings'
import { SettingsErrors } from '@/interfaces/responses'

@Component
export default class NotificationsSettings extends Vue {
  @Prop()
  errors!: SettingsErrors

  @Prop()
  notifications!: NotificationSettings

  changeNotification(event: Event): void {
    const checkbox = event.target as HTMLInputElement
    const notif = checkbox.dataset.name as keyof NotificationSettings
    const value = checkbox.checked
    this.$emit('changeNotification', { notification: notif, value })
  }
}
</script>
