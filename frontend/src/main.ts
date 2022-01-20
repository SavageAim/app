import Notifications from 'vue-notification'
import VModal from 'vue-js-modal'
import Vue from 'vue'
import VueCookies from 'vue-cookies'
import App from './App.vue'
import router from './router'
import store from './store'

Vue.config.productionTip = false
const dynamicDefaults = {
  adaptive: true,
  classes: 'card',
  height: 'auto',
  resizable: false,
  scrollable: true,
  styles: {
    'max-height': '80vh',
    'overflow-y': 'scroll',
  },
}
Vue.use(Notifications)
Vue.use(VModal, { dynamicDefaults })
Vue.use(VueCookies)

new Vue({
  render: (h) => h(App),
  router,
  store,
}).$mount('#app')
