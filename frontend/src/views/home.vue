<template>
  <div id="home" class="container-fluid">
    <template v-if="authenticated">
      <Dashboard />
    </template>
    <template v-else>
      <Welcome />
    </template>
  </div>
</template>

<script lang="ts">
import { Component } from 'vue-property-decorator'
import Dashboard from '@/components/dashboard.vue'
import Welcome from '@/components/welcome.vue'
import SavageAimMixin from '@/mixins/savage_aim_mixin'

@Component({
  components: {
    Dashboard,
    Welcome,
  },
})
export default class Home extends SavageAimMixin {
  mounted(): void {
    document.title = 'Savage Aim'
  }
}
</script>

<style lang="scss" scoped>
@import 'src/assets/variables.scss';

td {
  vertical-align: middle;
}

.media {
  align-items: center;
}

#team-table {
  & .icon {
    display: block;
  }

  & .buttons {
    margin-bottom: 0;

    & .button {
      margin-bottom: 0;
    }
  }
}
</style>
