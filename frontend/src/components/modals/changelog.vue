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
      <div class="divider"><i class="material-icons icon">expand_more</i> The Final Pre-Dawntrail (Non-Bugfix) Release <i class="material-icons icon">expand_more</i></div>
      <p>Good day fellow Warrior of Light, I hope that this message finds you well.</p>
      <p>I've been hard at work on some community requested features / changes, and on interesting new mechanics that I hope people will take advantage of for the new expansion!</p>
      <p>As a result, these patch notes are pretty large, but I encourage you to at least scroll through and read the various headings!</p>
      <p>Thank you to all who've been using my little passion project through Endwalker, and may you all have a good time in Dawntrail!</p>

      <div class="divider"><i class="material-icons icon">expand_more</i> Streamlined New User Experience <i class="material-icons icon">expand_more</i></div>
      <p>
        In the interest of making things easier for new Users to sign up and join their Teams, the following changes have been implemented to the system;
        <ul>
          <li>
            Characters can now use the site normally from the moment they are created, and no longer require being verified to interact with Teams/BIS Lists
            <ul>
              <li>The cleanup timer for Non-Verified Characters has been extended to 7 days, so be sure to verify eventually so you do not lose your Character!</li>
              <li>A Notification will be sent when a Character has not been verified in 5 days, to ensure you do not forget!</li>
            </ul>
          </li>
          <li>If you attempt to Create / Join a Team while your account has no Characters, there is now a form with two inputs. Providing your Character's Lodestone URL, and an Etro Gearset URL, will automatically create all the necessary details in one go!</li>
        </ul>
      </p>

      <div class="divider"><i class="material-icons icon">expand_more</i> Import from Lodestone <i class="material-icons icon">expand_more</i></div>
      <p>
        It is now possible to import your current gear from Lodestone when creating/editing BIS Lists!
        <ul>
          <li>If your current gear on Lodestone is not equippable by the Job your BIS List is set to, it will give a message and not make any changes.</li>
        </ul>
      </p>

      <div class="divider"><i class="material-icons icon">expand_more</i> Loot Manager - Solver <i class="material-icons icon">expand_more</i></div>
      <p>A new BETA feature has been added to the Loot Manager page; the Loot Solver.</p>
      <p>This feature aims to "solve" loot distibution by handing out loot fairly but in a way that ensures you spend the least number of weeks on each fight as possible.</p>
      <p>It is accessible in a dropdown box on the Loot Manager page, and you can see a full set of distribution for all of the required kills.</p>
      <p>People using the Per-Fight Loot Manager (accessible in User Settings) can also auto-assign the week's loot into the slots, allowing for an easy save if you're following it.</p>
      <p class="has-text-info">For more details, please see <a href="https://wiki.savageaim.com/teams/loot-solver" target="_blank">the wiki page</a> about this feature!</p>
      <p class="has-text-info">Because it is a Beta feature, there could be some algorithmic inconsistencies. If there are any issues or bugs or anything, please report them on the Discord!</p>

      <div class="divider"><i class="material-icons icon">expand_more</i> BIS List Actions Revamp <i class="material-icons icon">expand_more</i></div>
      <p>
        In the interest of improving UX, Action buttons that only affect part of the BIS Form have been moved to the relevant sections:
        <ul>
          <li>The "Import From Etro" button is now attached to the bottom of the BIS Gear section.</li>
          <li>Similarly, the "Import from Lodestone" and "Copy from Other List" buttons are now on the bottom of the Current Gear section.</li>
        </ul>
      </p>
      <p>The Actions box now only contains the Create/Save buttons, and the header of this box has been removed since it's now irrelevant to have one.</p>

      <div class="divider"><i class="material-icons icon">expand_more</i> Fixes & Improvements <i class="material-icons icon">expand_more</i></div>
      <p>Attempting to optimize queries on the Loot Manager page to improve performance!</p>
      <p>Converted PNG images to WebP format to give smaller images to download!</p>

      <div class="divider"><i class="material-icons icon">expand_more</i> Next Steps <i class="material-icons icon">expand_more</i></div>
      <p>SavageAim will be going for as long as I'm playing XIV, so this isn't some sort of closing down message!</p>
      <p>As always, I will be more than happy to talk through / work on feature requests from the community! After all, SavageAim wouldn't be this good without ideas from y'all!</p>
      <p>However, I would also like to try branching out.</p>
      <p>I'm thinking the next thing I could work on would be some sort of plugin that would allow you to sync current gear directly from in game.</p>
      <p>I have no idea how it would work or how much work it would involve but it would be something that I see myself using and that's all the motivation I need!</p>
      <p>If any of you have any other ideas you'd like to see within the SavageAim ecosystem, please don't hesitate to send a message!</p>
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
