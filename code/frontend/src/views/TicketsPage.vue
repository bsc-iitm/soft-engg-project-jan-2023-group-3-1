<template>
	<div>
		<h1>This is the tickets page</h1>
	</div>
	<div>
		<ticket v-for="ticket in tickets" :title="ticket.title" :desc="ticket.description"></ticket>
	</div>
</template>

<script>
	import axios from 'axios'
	import ticket from "../components/ticket.vue";
		export default {
			name: "TicketsPage",
			data:{
				ticket:[],
				port:'http://localhost:5000/'
			},
			components: {
				ticket
			},
			methods:{
				gettickets(){
					const path = 'tickets'
					axios.get(this.port+path)
					.then((res)=>{
						this.tickets = res.data
					})
				}
			},
			mounted() {
				this.gettickets()
			}
		}
</script>