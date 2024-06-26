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
  {
    path: '/characters/:characterId/',
    component: () => import('@/views/character.vue'),
    name: 'viewChar',
    props: true,
  },
  {
    path: '/characters/:characterId/bis_list/',
    component: () => import('@/views/new_bis.vue'),
    name: 'newBIS',
    props: true,
  },
  {
    path: '/characters/:characterId/bis_list/:bisId/',
    component: () => import('@/views/edit_bis.vue'),
    name: 'editBIS',
    props: true,
  },

  // Notifications
  { path: '/notifications/', component: () => import('@/views/notifications.vue'), name: 'userNotifs' },

  // User Settings
  { path: '/settings/', component: () => import('@/views/settings.vue'), name: 'userSettings' },

  // Team
  { path: '/team/', component: () => import('@/views/team/add.vue'), name: 'addTeam' },
  { path: '/team/new/', component: () => import('@/views/team/create.vue'), name: 'newTeam' },
  {
    path: '/team/:teamId/',
    component: () => import('@/views/team/overview.vue'),
    name: 'teamOverview',
    props: true,
  },
  {
    path: '/team/:teamId/loot/',
    component: () => import('@/views/team/loot.vue'),
    name: 'teamLoot',
    props: true,
  },
  {
    path: '/team/:teamId/management/',
    component: () => import('@/views/team/management.vue'),
    name: 'teamManagement',
    props: true,
  },
  {
    path: '/team/:teamId/member/:memberId/',
    component: () => import('@/views/team/manage_membership.vue'),
    name: 'teamMemberManage',
    props: true,
  },
  {
    path: '/team/:teamId/settings/',
    component: () => import('@/views/team/settings.vue'),
    name: 'teamSettings',
    props: true,
  },
  {
    path: '/team/join/:teamId/',
    component: () => import('@/views/team/join.vue'),
    name: 'teamJoin',
    props: true,
  },

  // Proxies
  {
    path: '/team/:teamId/proxies/',
    component: () => import('@/views/team/new_proxy.vue'),
    name: 'teamNewProxy',
    props: true,
  },
  {
    path: '/team/:teamId/proxies/:charId/',
    component: () => import('@/views/team/edit_proxy.vue'),
    name: 'teamEditProxy',
    props: true,
  },

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
  if (!anonymous && store.state.user.id === null) {
    next({ name: 'auth', params: { redirect: 'true', next: to.path } })
  }
  else next()
})

export default router
