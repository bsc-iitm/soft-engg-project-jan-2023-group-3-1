<template>
	<nav>
		<router-link to="/tickets">Tickets</router-link> |
		<router-link to="/faqs">FAQs</router-link>
	</nav>
	<div>
		<h1>This is the tickets page</h1>
	</div>
	<div>
		<ticket v-for="ticket in tickets" :title="ticket.title" :desc="ticket.description" :key="ticket.ticket_id"></ticket>
	</div>

	<add_ticket @added_ticket="gettickets()"></add_ticket>

	

</template>

<script>
	import axios from 'axios'
	import store from '@/store'
	import ticket from "../components/ticket.vue";
	import add_ticket from '@/components/add_ticket.vue';
	export default {
		name: "TicketsPage",
		data(){
			return {
				tickets:[],
				port:'http://localhost:5000/',
				current_user: {},
				auth_token: '',
				headers: {}
			}
		},
		components: {
			ticket,
			add_ticket
		},
		methods:{
			gettickets(){
				const path = 'tickets'
				axios.get(this.port+path,{headers:this.headers})
				.then((res)=>{
					this.tickets = res.data
				})
				.catch((rej)=>{
					console.log(rej)
				})
			},
			
		},
		async mounted() {
			this.current_user = store.state.user
			this.auth_token = store.state.auth_token
			this.headers = {
				'Content-Type': 'application/json',
				'Authentication-Token': this.auth_token
				}
			this.tickets = this.gettickets()
		}
	}
</script>