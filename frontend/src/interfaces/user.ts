import Notifications from './notifications'

export default interface User {
  avatar_url: string,
  id: number | null,
  notifications: Notifications,
  theme: string,
  username: string,
}
