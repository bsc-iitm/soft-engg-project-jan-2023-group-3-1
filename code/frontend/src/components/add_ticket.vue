<template>
	<div>
		<!-- Button trigger modal -->
		<button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#exampleModal">
			Add ticket
		</button>

	<!-- Modal -->
		<div class="modal fade" id="exampleModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
			<div class="modal-dialog" role="document">
				<div class="modal-content">
					<div class="modal-header">
						<h5 class="modal-title" id="exampleModalLabel">Describe your query</h5>
						<button type="button" class="close" data-bs-dismiss="modal" aria-label="Close">
							<span aria-hidden="true">&times;</span>
						</button>
					</div>
					<div class="modal-body">
						<form class="container px-5 text-center">
									<div class="mb-3 row justify-content-center">
										<label class="col-5 form-label text-lg-end">Title</label>
										<div class="col-5">
											<input type="text" name="Title" class="form-control" v-model="title" required/>
										</div>
										<div class="col-2"></div>
									</div>
									<div class="mb-3 row justify-content-center">
										<label class="col-5 form-label text-lg-end">Description</label>
										<div class="col-5">
											<input type="text" name="desc" class="form-control" v-model="description"/>
										</div>
										<div class="col-2"></div>
									</div>
						</form>
					</div>
					<div class="modal-footer">
					<button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
					<button type="button" class="btn btn-primary" v-on:click="addticket()">Submit</button>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
	import store from '@/store';
	import axios from 'axios'
    export default{
		name:"AddTicket",
		data(){
			return {
				current_user:{},
				auth_token: '',
				port:'http://localhost:5000/',
				headers: {},
				title: '',
				description: ''
			}
		},
        methods: {
			addticket(){
				const path = 'tickets'
				const data = {
					'title': this.title,
					'description': this.description
				}
				console.log(this.auth_token)
				axios.post(this.port+path,data,{headers:this.headers})
				.then((res)=>{
					this.$emit('added_ticket')
					console.log(res)
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
		}
    }
</script>