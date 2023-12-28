// Not your standard mixin, needs to be extended
import { Vue } from 'vue-property-decorator'
import QuickSwitcher from '@/components/modals/switcher.vue'
import User from '@/interfaces/user'

export default class SavageAimMixin extends Vue {
  LOGIN_URL = `/backend/accounts/discord/login/`
  LOGOUT_URL = `/backend/logout/`

  get authenticated(): boolean {
    return this.$store.state.user.id !== null
  }

  async load(): Promise<void> {
    console.error('unimplemented')
  }

  get user(): User {
    // This assumes that the User exists
    return this.$store.state.user
  }

  get modalContainer(): HTMLElement | null {
    return document.getElementById('modals-container')
  }

  getCloseButton(): HTMLLinkElement | null {
    // Convoluted function to get the button to click instead of just calling hide
    const modal = this.modalContainer?.getElementsByClassName('vm--modal')[0]
    return modal?.getElementsByClassName('icon')[0] as HTMLLinkElement
  }

  openSwitcher(): void {
    // Check if there's already an open modal
    if (this.modalContainer === null || this.modalContainer!.children.length === 0) {
      this.$modal.show(QuickSwitcher, { }, { closed: () => { this.load() } })
    }
    else {
      this.getCloseButton()!.click()
    }
  }

  handleError(statusCode: number): void {
    // Handle response error codes, redirecting as needed
    switch (statusCode) {
    case 400:
      break
    case 403:
      this.$router.push({ name: 'auth', params: { redirect: 'true' } })
      break
    case 404:
      // @ts-ignore
      this.$router.push({ name: 'errors/404', params: { catchAll: this.$route.path.split('/').slice(1) } })
      break
    case 500:
      this.$router.push({ name: 'errors/500' })
      break
    default:
      this.$notify({ text: `Unexpected HTTP Error Code; ${statusCode}.`, type: 'is-danger' })
    }
  }
}
