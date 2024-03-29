import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import "../node_modules/bootstrap/dist/css/bootstrap.css"
import "../node_modules/bootstrap/dist/js/bootstrap.bundle"
import store from './store'

router.beforeEach(async (to) => {
	console.log(store.state.logged_in)
	if (!store.state.logged_in && to.name !== 'Login') {
		return { name: 'Login' }
	}
})


const app = createApp(App)
app.use(router)
app.use(store)
app.mount('#app')
