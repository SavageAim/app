<template>
  <footer id="footer" class="content has-text-centered">
    <a class="kofi-link" href="https://ko-fi.com/eriyukidesu" target="_blank" data-microtip-position="top" role="tooltip" aria-label="Donate on Ko-Fi">
      <span class="icon is-large">
        <div class="icon-stack">
          <img src="/kofi-cup.svg" alt="Ko-Fi Logo" class="image is-24x24 cup" height="24" width="24" />
          <img src="/kofi-heart.svg" alt="Ko-Fi Logo" class="image is-24x24 heart" height="24" width="24" />
        </div>
      </span>
    </a>
    <a href="/backend/schema" target="_blank" data-microtip-position="top" role="tooltip" aria-label="API Schema"><span class="icon is-large"><i class="material-icons">api</i></span></a>
    <a href="https://wiki.savageaim.com" target="_blank" data-microtip-position="top" role="tooltip" aria-label="Wiki"><span class="icon is-large"><i class="material-icons">menu_book</i></span></a>
    <a data-microtip-position="top" role="tooltip" aria-label="Changelog" @click="showChangelog"><span class="icon is-large"><i class="material-icons">update</i></span></a>
    <a href="https://github.com/Savage-Aim/app" target="_blank" data-microtip-position="top" role="tooltip" aria-label="Github Repo"><span class="icon is-large"><i class="material-icons">code</i></span></a>
    <a href="https://github.com/Savage-Aim/plugin" target="_blank" data-microtip-position="top" role="tooltip" aria-label="Dalamud Plugin"><span class="icon is-large"><i class="material-icons">extension</i></span></a>
    <a class="discord-link" href="https://discord.gg/k8szJ5qAKw" target="_blank" data-microtip-position="top" role="tooltip" aria-label="Savage Aim Discord"><span class="icon is-large"><img src="/discord.svg" alt="Discord Logo" class="image is-24x24 discord" height="24" width="24" /></span></a>
    <p>Savage Aim release {{ $store.state.version }}, by Eira Erikawa (Lich)</p>
    <p>FINAL FANTASY XIV ©2010 - {{ currentYear }} SQUARE ENIX CO., LTD. All Rights Reserved.</p>
    <p>FINAL FANTASY is a registered trademark of Square Enix Holdings Co., Ltd. All material used under license.</p>
  </footer>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import Changelog from '@/components/modals/changelog.vue'

// Simple legal + handy links footer bit
// Sorta stolen from Etro
@Component
export default class Footer extends Vue {
  get currentYear(): number {
    return (new Date()).getFullYear()
  }

  showChangelog(): void {
    this.$modal.show(Changelog)
  }
}
</script>

<style lang="scss">
#footer {
  padding-top: 1em;

  & p {
    margin-bottom: 0;
    font-size: 0.85em;
    font-weight: 300;
    line-height: 1.1;
  }

  & a {
    color: white;

    &:hover {
      color: #346CC3;
    }
  }
}

.discord-link:hover .image {
  filter: brightness(0) saturate(100%) invert(37%) sepia(36%) saturate(3088%) hue-rotate(220deg) brightness(95%) contrast(99%);
}

.icon-stack {
  position: relative;

  & .cup {
    position: absolute;
    top: 0;
    left: 0;
    z-index: -10;
  }
}

.kofi-link:hover {
  & .cup {
    filter: brightness(0) saturate(100%) invert(47%) sepia(36%) saturate(1001%) hue-rotate(312deg) brightness(100%) contrast(101%);
  }

  & .heart {
    filter: brightness(0) saturate(100%) invert(98%) sepia(0%) saturate(0%) hue-rotate(233deg) brightness(102%) contrast(104%);
  }
}
</style>
