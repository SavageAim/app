import * as Sentry from '@sentry/vue'
import Vue from 'vue'
import Notifications from 'vue-notification'
import VModal from 'vue-js-modal'
import VueCookies from 'vue-cookies'
import VueShortkey from 'vue-shortkey'
import App from './App.vue'
import router from './router'
import store from './store'

Vue.config.productionTip = false
const dynamicDefaults = {
  adaptive: true,
  classes: 'card',
  height: 'auto',
  width: '800px',
  resizable: false,
  scrollable: true,
  styles: {
    'max-height': '80vh',
    'overflow-y': 'auto',
  },
}
Vue.use(Notifications)
Vue.use(VModal, { dynamicDefaults })
Vue.use(VueCookies)
Vue.use(VueShortkey)

Sentry.init({
  Vue,
  dsn: 'https://06f41b525a40497a848fb726f6d03244@o242258.ingest.sentry.io/6180221',
  logErrors: true,
  release: 'savageaim@20250108',
  integrations: [
    Sentry.browserTracingIntegration(),
    Sentry.replayIntegration(),
    Sentry.feedbackIntegration({
      colorScheme: 'dark',
      showName: false,
      showEmail: false,
      showBranding: false,
      triggerLabel: 'Feedback',
      formTitle: 'Send us Feedback',
      submitButtonLabel: 'Send',
      messageLabel: 'Message',
      messagePlaceholder: 'What would you like to tell us?',
      themeDark: {
        background: '#17181c',
        foreground: '#F3F3EC',
        accentForeground: '#F3F3EC',
        accentBackground: '#5d98c4',
        successColor: '#4E9381',
        errorColor: '#c14762',
        outline: '0.5px solid #2E53A5',
      },
    }),
  ],
  tracesSampleRate: 0.5,

  // Only capture replays for errors
  replaysSessionSampleRate: 0,
  replaysOnErrorSampleRate: 1,
})

new Vue({
  render: (h) => h(App),
  router,
  store,
}).$mount('#app')
