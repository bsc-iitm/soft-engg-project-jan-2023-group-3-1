<template>
	<div >
		<nav>
			<h1>This is the FAQs page</h1>
			<router-link to="/tickets">Tickets</router-link> |
			<router-link to="/faqs">FAQs</router-link>
		</nav>
		<div class="row">
			<add_faq v-if="current_user.role == 'Admin'" @added_faq="getfaqs()"></add_faq>
		</div>
		<div class="row">
			<div class="col-3">
				Filter By: <input v-model="search">	
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
