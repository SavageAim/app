import Vue from 'vue'
import VueRouter from 'vue-router'
import Auth from './views/auth.vue'
import Home from './views/home.vue'
import store from './store'

// Import our components and give them routes.

Vue.use(VueRouter)

const routes = [
  // Home
  {
    path: '/',
    component: Home,
    name: 'home',
    meta: { anon: true },
  },

  // Auth
  {
    path: '/auth/',
    component: Auth,
    name: 'auth',
    props: true,
    meta: { anon: true },
  },

  // Character
  { path: '/characters/new/', component: () => import('@/views/new_char.vue'), name: 'newChar' },
  { path: '/characters/:id/', component: () => import('@/views/character.vue'), name: 'viewChar' },
  { path: '/characters/:characterId/bis_list/', component: () => import('@/views/new_bis.vue'), name: 'newBIS' },
  { path: '/characters/:characterId/bis_list/:id/', component: () => import('@/views/edit_bis.vue'), name: 'editBIS' },

  // Notifications
  { path: '/notifications/', component: () => import('@/views/notifications.vue'), name: 'userNotifs' },

  // User Settings
  { path: '/settings/', component: () => import('@/views/settings.vue'), name: 'userSettings' },

  // Team
  { path: '/team/', component: () => import('@/views/team/add.vue'), name: 'addTeam' },
  { path: '/team/new/', component: () => import('@/views/team/create.vue'), name: 'newTeam' },
  { path: '/team/:id/', component: () => import('@/views/team/details.vue'), name: 'teamDetails' },
  { path: '/team/:id/loot/', component: () => import('@/views/team/loot.vue'), name: 'teamLoot' },
  { path: '/team/:id/management/', component: () => import('@/views/team/management.vue'), name: 'teamManage' },
  {
    path: '/team/:teamId/member/:id/',
    component: () => import('@/views/team/manage_membership.vue'),
    name: 'teamMemberManage',
  },
  { path: '/team/:id/settings/', component: () => import('@/views/team/settings.vue'), name: 'teamSettings' },
  { path: '/team/join/:id/', component: () => import('@/views/team/join.vue'), name: 'teamJoin' },

  // Errors
  { path: '/errors/500/', component: () => import('@/views/errors/500.vue'), name: 'errors/500' },
  { path: '/:catchAll(.*)*', component: () => import('@/views/errors/404.vue'), name: 'errors/404' },
]

const router = new VueRouter({
  linkExactActiveClass: 'is-active',
  mode: 'history',
  routes,
})

router.beforeEach(async (to, from, next) => {
  const anonymous = (to.meta || { anon: false }).anon
  if (!store.state.userLoaded) await store.dispatch('fetchUser')
  if (!anonymous && store.state.user.id === null) next({ name: 'auth', params: { redirect: 'true' } })
  else next()
})

export default router
