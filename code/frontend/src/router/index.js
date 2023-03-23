import { createRouter, createWebHistory } from 'vue-router'
import FAQs from '../views/FAQs.vue'

const routes = [
  {
    path: '/faqs',
    name: 'FAQs',
    component: FAQs
  },
  {
    path: '/',
    name: 'Tickets',
    component: () => import('../views/TicketsPage.vue')
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
