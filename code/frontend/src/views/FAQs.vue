<template>
	<div >
		<nav>
			<h1>This is the tickets page</h1>
			<router-link to="/tickets">Tickets</router-link> |
			<router-link to="/faqs">FAQs</router-link>
		</nav>
		<div class="row">
			<add_faq @added_faq="getfaqs()"></add_faq>
		</div>
		<div class="row">
			<div class="col-2">
				Filter By: <input v-model="search">	
			</div>
			<div class="col-8 mb-3">
				<ticket @ticket_edited="update_ticket(ticket.ticket_id)" v-for="ticket in filtered" :ticket="ticket" :key="ticket.ticket_id"></ticket>
			</div>
		</div>

	</div>

</template>

<script>
	import axios from 'axios'
	import store from '@/store'
	import ticket from "../components/ticket.vue";
	import add_faq from '@/components/add_faq.vue';
	export default {
		name: "FAQs",
		data(){
			return {
				faqs:[],
				port:'http://localhost:5000/',
				current_user: {},
				auth_token: '',
				headers: {},
				question: '',
				answer: '',
				search: ''
			}
		},
		computed: {
			filtered() {
				if(!this.tickets){
					return []
				}
				return this.tickets.filter((item) => item.title.includes(this.search));
			}
		},
		components: {
			ticket,
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
			}
		},
		async mounted() {
			this.current_user = store.state.user
			this.auth_token = store.state.auth_token
			this.headers = {
				'Content-Type': 'application/json',
				'Authentication-Token': this.auth_token
				}
			this.faqs = this.getfaqs()
		}
	}
</script>
