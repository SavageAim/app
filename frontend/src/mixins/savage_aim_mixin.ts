// Not your standard mixin, needs to be extended
import { Vue } from 'vue-property-decorator'
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
