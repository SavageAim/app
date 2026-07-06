<template>
  <footer id="footer" class="content has-text-centered">
    <a class="patreon-link" href="https://www.patreon.com/cw/freyamade" target="_blank" data-microtip-position="top" role="tooltip" aria-label="Support SavageAim on Patreon"><span class="icon is-large"><img src="/patreon.svg" alt="Patreon Logo" class="image is-24x24" height="24" width="24" /></span></a>
    <a :href="`${baseUrl}/backend/schema`" target="_blank" data-microtip-position="top" role="tooltip" aria-label="API Schema"><span class="icon is-large"><i class="material-icons">api</i></span></a>
    <a href="https://wiki.savageaim.com" target="_blank" data-microtip-position="top" role="tooltip" aria-label="Wiki"><span class="icon is-large"><i class="material-icons">menu_book</i></span></a>
    <a data-microtip-position="top" role="tooltip" aria-label="Changelog" @click="showChangelog"><span class="icon is-large"><i class="material-icons">update</i></span></a>
    <a href="https://github.com/SavageAim/app" target="_blank" data-microtip-position="top" role="tooltip" aria-label="Github Repo"><span class="icon is-large"><i class="material-icons">code</i></span></a>
    <a href="https://github.com/SavageAim/plugin" target="_blank" data-microtip-position="top" role="tooltip" aria-label="Dalamud Plugin"><span class="icon is-large"><i class="material-icons">extension</i></span></a>
    <a class="discord-link" href="https://discord.gg/k8szJ5qAKw" target="_blank" data-microtip-position="top" role="tooltip" aria-label="Savage Aim Discord"><span class="icon is-large"><img src="/discord.svg" alt="Discord Logo" class="image is-24x24 discord" height="24" width="24" /></span></a>
    <p>Savage Aim release {{ $store.state.version }}, by Eira Suzumori (Lich)</p>
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

  get baseUrl(): string {
    return process.env.VUE_APP_URL
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
    color: hsl(60, 13%, 88%);

    &:hover {
      color: #346CC3;
    }
  }
}

.patreon-link {
  & .image {
    filter: invert(94%) sepia(6%) saturate(590%) hue-rotate(339deg) brightness(109%) contrast(79%);
  }

  &:hover .image {
    filter: invert(39%) sepia(12%) saturate(4471%) hue-rotate(184deg) brightness(94%) contrast(89%);
  }
}

.discord-link:hover .image {
  filter: brightness(0) saturate(100%) invert(37%) sepia(36%) saturate(3088%) hue-rotate(220deg) brightness(95%) contrast(99%);
}
</style>
