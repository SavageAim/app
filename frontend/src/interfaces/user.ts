import NotificationSettings from './notification_settings'

export default interface User {
  avatar_url: string,
  id: number | null,
  loot_manager_version: string,
  loot_solver_greed: boolean,
  notifications: NotificationSettings,
  token: string | null,
  theme: string,
  username: string,
}
