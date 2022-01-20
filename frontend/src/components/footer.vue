<template>
  <footer id="footer" class="content has-text-centered">
    <a href="#changelog" class="has-text-white" title="Changelog" @click="showChangelog"><span class="icon is-large"><i class="material-icons">update</i></span></a>
    <p>Savage Aim, by Erika Yukiko (Lich)</p>
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
}
</style>
