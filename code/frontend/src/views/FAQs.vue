<template>
	<div >
		<div class="row">
			<h1 class="col">FAQs</h1>
			<div class="col text-end p-3">
				<router-link class="btn btn-outline-dark" to="/tickets">Tickets</router-link>
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
				Filter By: <input class="form-control" v-model="search">	
				<add_faq v-if="current_user.role == 'Admin'" @added_faq="getfaqs()"></add_faq>
			</div>
			<div class="col-8 mb-3">
				<faq @faq_edited="update_faq(faq.f_id)" v-for="faq in filtered" :faq="faq" :key="faq.f_id"></faq>
			</div>
		</div>

	</div>

</template>

<script>
	import axios from 'axios'
	import store from '@/store'
	import router from '@/router'
	import faq from "../components/faq.vue";
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
				if(!this.faqs){
					return []
				}
				return this.faqs.filter((item) => item.question.includes(this.search));
			}
		},
		components: {
			faq,
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
			update_faq(f_id){
				const path = `faqs/${f_id}`
				axios.get(this.port+path,{headers:this.headers})
				.then((res)=>{
					for(let i=0;i<this.faqs.length;i++){
						if(this.faqs[i].f_id == f_id){
							this.faqs[i] = res.data
						}
					}
				}) 
				.catch((rej)=>{
					if(rej.response.status === 404){
						for(let i=0;i<this.faqs.length;i++){
							if(this.faqs[i].f_id === f_id){
								this.faqs.splice(i, 1);
							}
						}	
					}
				})
			},
			logout(){
				store.commit('logout')
				console.log(store.state.logged_in)
				router.push('/')
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
