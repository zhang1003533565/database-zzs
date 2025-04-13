import { createRouter, createWebHistory } from 'vue-router'

// 这里是所有页面路由
const routes = [
  { path: '/', component: () => import('@/views/HomePage.vue') },
  { path: '/health-organization', component: () => import('@/views/HealthOrganization.vue') },
  { path: '/main-index', component: () => import('@/views/MainIndex.vue') },
  { path: '/rural-organization', component: () => import('@/views/RuralOrganization.vue') },
  { path: '/tech-application', component: () => import('@/views/TechApplication.vue') },
  { path: '/total-value', component: () => import('@/views/TotalValue.vue') },
  { path: '/total-agriculture', component: () => import('@/views/TotalAgriculture.vue') },
  { path: '/agent-page', component: () => import('@/views/AgentPage.vue') }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
