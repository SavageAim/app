import NotificationSettings from './notification_settings'

export default interface User {
  avatar_url: string,
  id: number | null,
  loot_manager_version: string,
  notifications: NotificationSettings,
  token: string | null,
  theme: string,
  username: string,
}
