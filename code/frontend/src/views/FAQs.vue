<template>
	<div >
		<nav>
			<h1>This is the FAQ's page</h1>
			<router-link to="/tickets">Tickets</router-link> |
			<router-link to="/faqs">FAQs</router-link>
		</nav>
		<div class="row">
			<add_faq @added_faq="getfaq()"></add_faq>
		</div>

	</div>

</template>

<script>
	import axios from 'axios'
	import store from '@/store'
	import add_faq from '@/components/add_faq.vue';

	export default {
		name: "FAQsPage",
		data(){
			return {
				faqs:[],
				port:'http://localhost:5000/',
				current_user: {},
				auth_token: '',
				headers: {},
				title: '',
				desc: '',
				search: '',
				filters: ['All','Open','Closed'],
				activeFilter: 'All'
			}
		},

		components: {
			add_faq
		},
		methods:{
			getfaqs(){
				const path = 'faqs'
				axios.get(this.port+path,{headers:this.headers})
				.then((res)=>{
					this.faqs = res.data
				})
				.catch((rej)=>{
					console.log(rej)
				})
			},
			addfaq(){
				const path = 'faqs'
				console.log(this.headers)
				axios.post(this.port+path,{title: this.title, description: this.desc},{headers:this.headers})
				.then((res)=>{
					console.log(res)
					this.faqs = this.getfaq()
				})
			},
			update_faq(faq_id){
				const path = `faq/${faq_id}`
				axios.get(this.port+path,{headers:this.headers})
				.then((res)=>{
					console.log(res)
					for(let i=0;i<this.faqs.length;i++){
						if(this.faq[i].faq_id == faq_id){
							this.faqs[i] = res.data
						}
					}
				}) 
				.catch((rej)=>{
					console.log(rej)
				})
			}
		},
		async mounted() {
			this.current_user = store.state.user
			this.auth_token = store.state.auth_token
			this.headers = {
				'Content-Type': 'application/json',
				'Authentication-Token': this.auth_token
				}
			this.tickets = this.getfaqs()
		}
	}
</script>
	