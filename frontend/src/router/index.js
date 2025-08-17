import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../components/Dashboard.vue'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard
  },
  {
    path: '/devices',
    name: 'Devices',
    component: () => import('../components/DeviceList.vue')
  },
  {
    path: '/data',
    name: 'Data',
    component: () => import('../components/DataTable.vue')
  },
  {
    path: '/events',
    name: 'Events',
    component: () => import('../components/EventLog.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
