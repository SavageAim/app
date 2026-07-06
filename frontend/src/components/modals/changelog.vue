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
      <div class="divider"><i class="material-icons icon">expand_more</i> Remigration <i class="material-icons icon">expand_more</i></div>
      <p>Turns out trying to move the system to a deployment mechanism that only spins up the server when it's needed was not cheaper.</p>
      <p>I've moved SavageAim back to simple containers on a single VM, which not only saves money but brings back all the real-time update stuff!</p>
      <p>Should have obeyed the timeless rule of "If it ain't broke don't fix it", but at least I have a better understanding of cloud products now as a result!</p>
      <p>
        <ul>
          <li>The Patreon should now have a much easier time covering costs.</li>
          <li>A massive thank you to everyone who has supported the project already!</li>
          <li>If it starts to out-perform the running costs, I'll invest the extra into useful upgrades.</li>
          <li>If you have any suggestions for these upgrades, please feel free to let me know!</li>
        </ul>
      </p>
      <p>Thank you all for sticking by the project this long, hopefully it stays around for a long time to come!</p>
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

<style lang="scss">
</style>
