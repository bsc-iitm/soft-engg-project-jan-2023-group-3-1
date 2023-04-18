<template>
	<div >
		<nav>
			<h1>This is the tickets page</h1>
			<router-link to="/tickets">Tickets</router-link> |
			<router-link to="/faqs">FAQs</router-link>
		</nav>
		<div class="row">
			<add_ticket @added_ticket="gettickets()"></add_ticket>
		</div>
		<div class="row">
			<div class="col-2">
				Filter By: <input v-model="search">	
			</div>
			<div class="tags-wrapper">
				<div v-for="(filter, index) in filters" :key="index">
					<button @click="this.activeFilter=filter" :class="{ active: filter === this.activeFilter }">{{ filter }}</button>
				</div>
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
	import add_ticket from '@/components/add_ticket.vue';
	export default {
		name: "TicketsPage",
		data(){
			return {
				tickets:[],
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
		computed: {
			filtered() {
				if (this.activeFilter === 'All') {
					return this.tickets.filter((item) => item.title.includes(this.search));
				}
				
				return this.tickets.filter((item) => item.status === this.activeFilter.toLowerCase()).filter((item) => item.title.includes(this.search));
				
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
			addticket(){
				const path = 'tickets'
				console.log(this.headers)
				axios.post(this.port+path,{title: this.title, description: this.desc},{headers:this.headers})
				.then((res)=>{
					console.log(res)
					this.tickets = this.gettickets()
				})
			},
			update_ticket(ticket_id){
				const path = `ticket/${ticket_id}`
				axios.get(this.port+path,{headers:this.headers})
				.then((res)=>{
					console.log(res)
					for(let i=0;i<this.tickets.length;i++){
						if(this.tickets[i].ticket_id == ticket_id){
							this.tickets[i] = res.data
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
			this.tickets = this.gettickets()
		}
	}
</script>