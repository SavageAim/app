<template>
  <div>
    <div class="card-header">
      <div class="card-header-title">
        Changelog
      </div>
      <div class="card-header-icon">
        <a @click="() => { this.$emit('close') }" class="icon">
          <i class="material-icons">close</i>
        </a>
      </div>
    </div>
    <div class="card-content content">
      <h2 class="has-text-primary subtitle">{{ version }}</h2>
      <div class="divider"><i class="material-icons icon">expand_more</i> Team Permissions <i class="material-icons icon">expand_more</i></div>
      <p>Added the ability for Team Leaders to extend certain permissions to other Members of the Team.</p>
      <p>
        The permissions currently available are as follows;
        <ul>
          <li>Handing out / Tracking Loot in the Loot Manager page.</li>
          <li>Management of Team Owned Characters (see below).</li>
        </ul>
      </p>
      <p>Permissions are editable by Team Leaders and viewable by Team Members in the new Management page.</p>

      <div class="divider"><i class="material-icons icon">expand_more</i> Team Owned Characters <i class="material-icons icon">expand_more</i></div>
      <p>There are many circumstances as to why some members of a Team will not sign up on the site.</p>
      <p>To allow Team Leaders to still track and manage BIS Lists of these members, Team Owned Characters can now be created via the Management page.</p>
      <p>These will be displayed in the Team List similarly to the other Characters, albeit with an icon indicating that they are Team Owned.</p>
      <p>If the owner does sign up later, they can claim the Character from the Teams that have it seamlessly!</p>
      <p>For more information, please visit the <a href="https://wiki.savageaim.com/teams/member-management">wiki</a>!</p>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'

@Component
export default class Changelog extends Vue {
  get version(): string {
    return this.$store.state.version
  }
}
</script>
