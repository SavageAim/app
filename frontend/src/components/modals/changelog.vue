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

      <div class="divider"><i class="material-icons icon">expand_more</i> FFXIV Patch 6.2 Released! <i class="material-icons icon">expand_more</i></div>
      <p>A new Tier, Pandæmonium: Abyssos, has been added. Please ensure to update your Team to the new Tier to have BIS Table colours display correctly!</p>
      <p>All the gear added with Patch 6.2 has been added to the site, please enjoy updating your BIS Lists for the new Tier!</p>
      <p>The default values for the Item Level filters in BIS pages have been updated to the new range for Abyssos. (610 - 635)</p>

      <div class="divider"><i class="material-icons icon">expand_more</i> Team Member Permissions <i class="material-icons icon">expand_more</i></div>
      <p>The ability to give extra permissions within a Team has been added.</p>
      <p>These can be controlled via the "Manage Members" page of a Team.</p>
      <p>
        Currently the available permissions are;
        <ul>
          <li>Loot Manager - Allow a Member to track and hand out Loot via the Loot Manager!</li>
          <li>Proxy Manager - Allow a Member to add / edit / remove Proxy Characters from the Team!</li>
        </ul>
      </p>

      <div class="divider"><i class="material-icons icon">expand_more</i> Team Member Management Page <i class="material-icons icon">expand_more</i></div>
      <p>A new page has been added to Teams; Manage Members!</p>
      <p>This page is solely responsible for the management of all Members of a Team.</p>
      <p>
        Team Members can use this page to;
        <ul>
          <li>See their and other Members' permissions within the Team.</li>
        </ul>
      </p>
      <p>
        Team Leaders can also use this page to;
        <ul>
          <li>Manage Permissions of non-Proxy Members.</li>
          <li>Kick Members from the Team.</li>
        </ul>
      </p>
      <p>Members with the "Proxy Manager" permission will also have the ability to Add, Edit, and Kick Proxy Characters.</p>

      <div class="divider"><i class="material-icons icon">expand_more</i> Minor Changes <i class="material-icons icon">expand_more</i></div>
      <p>Renamed "Team Details" to "Team Overview" in the Team Navigation bar.</p>
      <p>Removed the "Add Proxy Character" from the Overview page as it is now handled in the Management page.</p>
      <p>Removed the "Edit Proxy" and "Kick from Team" items from the "Actions" dropdown in "Team Overview" as these have been moved to Management page.</p>
      <p>
        Changed some text of remaining items in the "Actions" dropdown to be more clear;
        <ul>
          <li>"Edit List" -> "Edit BIS List"</li>
          <li>"Change Character" -> "Change Linked Character / BIS List"</li>
        </ul>
      </p>
      <p>Fixed issue where Team Leaders would have both the Leader and Member icon displayed in the Overview page.</p>
      <p>Fixed issue where live reloading wasn't happening when intended.</p>
      <p>
        Added some more pride flag colour schemes.
        <ul>
          <li>I added as many as I could get to realistically work and still be noticeable, but if you have suggestions for others then please let me know in the Discord! &lt;3</li>
        </ul>
      </p>
      <p>Fixed issue where certain parts of the Edit Proxy page were not displaying information correctly.</p>
      <p>Team Create and Join pages now have special handling for when the user has no Characters yet.</p>

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
