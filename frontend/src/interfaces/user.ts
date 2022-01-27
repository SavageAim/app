import NotificationsSettings from './notifications_settings'

export default interface User {
  avatar_url: string,
  id: number | null,
  notifications: NotificationsSettings,
  theme: string,
  username: string,
}
