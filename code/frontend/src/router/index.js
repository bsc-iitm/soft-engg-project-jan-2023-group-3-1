import { createRouter, createWebHistory } from 'vue-router'
import login from '../views/login.vue'
import FAQs from '../views/FAQs.vue'
import TicketsPage from '../views/TicketsPage.vue'
import FaqList from '../components/FaqList.vue'

const routes = [
	{
		path:'/',
		name: 'Login',
		component: login
	},
	{
		path: '/faqs',
		name: 'FAQs',
		component: FAQs
	},

	{
		path: '/faqss',
		name: 'FaqList',
		component: FaqList
	},
	{
		path: '/tickets',
		name: 'Tickets',
		component: TicketsPage
	}
]

const router = createRouter({
	history: createWebHistory(process.env.BASE_URL),
	routes
})


export default router
