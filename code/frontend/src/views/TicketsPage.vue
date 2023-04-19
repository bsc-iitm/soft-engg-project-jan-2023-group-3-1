<template>
	<div>
		<div class="row">
			<h1 class="col">Tickets</h1>
			<div class="col text-end p-3">
				<router-link class="btn btn-outline-dark" to="/faqs">FAQs</router-link>
				<button type="button" class="btn btn-link-dark" data-bs-toggle="modal" data-bs-target="#profile">
					<i class="fa-solid fa-user fa-2xl"></i>
				</button>

				<div class="modal fade profile-int" id="profile" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true" data-bs-backdrop="false">
					<div class="modal-dialog position-absolute" role="document">
						<div class="modal-content">
							<div class="modal-header">
								<h4 class="modal-title">User Profile</h4>
								<button class="btn btn-outline-danger" data-bs-dismiss="modal">
									<i class="fa-solid fa-xmark"></i>
								</button>
							</div>
							<div class="modal-body">
								<p>Username: {{ current_user.username }}</p>
								<p>Email: {{ current_user.email }}</p>
								<p>Role: {{ current_user.role }}</p>
								<button class="btn btn-outline-danger" @click="logout()">Logout</button>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>

		<div class="row">
			<div class="col-3">
				<div class="row p-3">
					Filter By: <input class="form-control" v-model="search">	
				</div>
				<div class="row p-3">
					Limit to: <input class="form-control" v-model="limit">	
				</div>
				<div class="container">
					<label class="ps-3 pe-3" for="all">All</label>
					<input type="radio" id="all" value="all" v-model="ticket_status" />
					
					<label class="ps-3 pe-3" for="openonly">Open</label>
					<input type="radio" id="openonly" value="open" v-model="ticket_status" />
					
					<label class="ps-3 pe-3" for="closedonly">Closed</label>
					<input type="radio" id="closedonly" value="closed" v-model="ticket_status" />
					
					<label class="p-3" for="useronly">My tickets</label>
					<input type="checkbox" id="useronly" v-model="useronly" />
				</div>
				<div class="p-3">
					<label for="sorter">Sort by:</label>
					<select class="form-select" v-model="sortby" id="sorter">
						<option disabled value="">Please select one</option>
						<option>upvotes</option>
						<option>last modified</option>
						<option>date created</option>
						<option>date completed</option>
					</select>
				</div>
				<add_ticket v-if="current_user.role == 'Student'" @added_ticket="gettickets()"></add_ticket>
			</div>
			<div class="col-8 mb-3">
				<ticket @ticket_edited="update_ticket(ticket.ticket_id)" v-for="ticket in filtered.slice(0,limit)" :ticket="ticket" :key="ticket.ticket_id"></ticket>
			</div>
		</div>

	</div>

</template>

<script>
	import axios from 'axios'
	import store from '@/store'
	import router from '@/router'
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
				limit: 100,
				ticket_status:'all',
				useronly:false,
				sortby:'last modified',
			}
		},
		computed: {
			filtered() {
				if (!this.tickets){
					return []
				}
				let filter_tickets = [...this.tickets]
				
				filter_tickets = filter_tickets.filter((item)=> item.title.includes(this.search))
				
				if (this.useronly) {
					filter_tickets = filter_tickets.filter((item) => item.user.id === this.current_user.id 
													|| (item.status == 'closed' && item.staff.id == this.current_user.id))

				}
				if (this.ticket_status !== 'all') {
					filter_tickets = filter_tickets.filter((item) => item.status === this.ticket_status.toLowerCase());
				}
				if( this.sortby == 'upvotes'){
					filter_tickets = filter_tickets.sort((first,second)=>{
						return second.upvotes - first.upvotes;
					})
				}
				if(this.sortby == 'last modified'){
					filter_tickets = filter_tickets.sort((first,second)=>{
						let second_date = new Date(second.last_modified)
						let first_date = new Date(first.last_modified)
						return second_date-first_date;
					})
				}
				if(this.sortby == 'date created'){
					filter_tickets = filter_tickets.sort((first,second)=>{
						let second_date = new Date(second.date_created)
						let first_date = new Date(first.date_created)
						return second_date-first_date;
					})
				}
				if(this.sortby == 'date closed'){
					filter_tickets = filter_tickets.sort((first,second)=>{
						let second_date = new Date(second.date_created)
						let first_date = new Date(first.date_created)
						return second_date-first_date;
					})
				}
				return filter_tickets
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
					for(let i=0;i<this.tickets.length;i++){
						if(this.tickets[i].ticket_id == ticket_id){
							this.tickets[i] = res.data
						}
					}
				}) 
				.catch((rej)=>{
					if(rej.response.status === 404){
						for(let i=0;i<this.tickets.length;i++){
							if(this.tickets[i].ticket_id === ticket_id){
								this.tickets.splice(i, 1);
							}
						}	
					}
				})
			},
			logout(){
				store.commit('logout')
				console.log('the user is',store.state.logged_in)
				router.push('/')
			}
		},
		updated(){
			this.current_user = store.state.user
			this.auth_token = store.state.auth_token
			this.headers = {
				'Content-Type': 'application/json',
				'Authentication-Token': this.auth_token
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

<style>
	.modal-dialog {
		right:10px;
		top: 30px;
	}
	.profile-int {
		pointer-events: none;
	}
	.modal-open {
		overflow-y: auto;
	}
	.profile-int .modal-backdrop {
		display: none;
	}
	.navigation-bar {
		background: #757474;
	}
</style>