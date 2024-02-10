<template>
  <div class="container">
    <div class="card">
      <div class="card-header">
        <div class="card-header-title is-centered">
          <figure class="image is-64x64">
            <img ref="materia" class="is-rounded" :src="`/materia/${cls}.png`" alt="Savage Aim Materia Logo" width="64" height="64" @click="changeMateria" />
          </figure>
          <h2 class="title">Savage <span :class="`has-text-${cls}`" class="ease">Aim</span></h2>
        </div>
      </div>
      <div class="card-content has-text-centered">
        <p>SavageAim is a tool used for managing the Best-in-Slot (BiS) lists of Savage Prog groups in FFXIV.</p>
        <p>It is designed by someone who raids primarily blind, and initially was constructed with my own static's interests first and foremost.</p>
        <p>However, as the project has gotten bigger, more feedback has been given by people and it is developing into a system that I hope everyone can be happy to use!</p>
        <p>I welcome you to the site, and ask only that if you have some feedback or assistance, please make it known through the Discord server so I can continue to make this tool better in the future!</p>
        <p>The wiki link in the footer is also a handy place where all of the running of the tool has been documented as it is being developed.</p>
        <hr />
        <p>Happy raiding! :D</p>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'

@Component
export default class Welcome extends Vue {
  cls = 'danger'

  clsList = [
    'danger',
    'info',
    'primary',
    'success',
    'warning',
  ]

  get materia(): HTMLElement {
    return this.$refs.materia as HTMLElement
  }

  changeMateria(): void {
    if (this.materia.classList.contains('spin')) return
    this.materia.classList.add('spin')
    window.setTimeout(this.clsChange, 350)
    window.setTimeout(this.stopSpin, 1200)
  }

  clsChange(): void {
    // Record the current cls so we don't pick it again
    const current = this.clsList.indexOf(this.cls)
    let newIndex = current
    while (newIndex === current) {
      newIndex = Math.floor(Math.random() * this.clsList.length)
    }
    this.cls = this.clsList[newIndex]
  }

  stopSpin(): void {
    this.materia.classList.remove('spin')
  }
}
</script>

<style lang="scss" scoped>
@-moz-keyframes spin {
    10% { -moz-transform: rotate(15deg); }
    100% { -moz-transform: rotate(-360deg); }
}
@-webkit-keyframes spin {
    10% { -webkit-transform: rotate(15deg); }
    100% { -webkit-transform: rotate(-360deg); }
}
@keyframes spin {
    10% {
        -webkit-transform: rotate(15deg);
        transform:rotate(15deg);
    }
    100% {
        -webkit-transform: rotate(-360deg);
        transform:rotate(-360deg);
    }
}

.card-header-title .title {
  font-weight: 300;
  padding-left: 1rem;
}

img.spin {
  animation-name: spin;
  animation-duration: 1.2s;
}

span.ease {
  transition: color 0.4s ease;
}
</style>
