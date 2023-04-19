<template>
    <h1 class="text-center fw-bold display-1">Ticketing system</h1>
    <div class="container mb-3 col-6 text-center display-6">
        <div class="fs-div" id="email">
            <label for="email">Email Address</label>
            <input autocomplete="email" class="form-control" type="email" v-model="email">
        </div>
    </div>
    <div class="container mb-3 col-6 text-center display-6">
        <div class="fs-div" id="email">
            <label for="email">Password</label>
            <input class="form-control" type="password" v-model="password">
        </div>
    </div>
    
    <div class="container mb-3 col-6 text-center display-6">
        <div class="text-danger" style="font-size:large;">
            <p v-for="error in errors" :key="error" >{{ error }}</p>
        </div>
    </div>

    <div class="py-3 text-center">
        <input v-on:click="login(email,password)" type="submit" value = "Submit" class="btn btn-primary mb-3">
    </div>
    <p class="text-center">Don't have an account? <a href = 'http://localhost:5000/register'>Sign up</a></p>
    
</template>

<script>
    import router from '@/router';
    import store from '@/store';
    import axios from 'axios'
    export default {
        name:'LoginPage',
        data() {
            return {   
            email:'',
            password:'',
            remember:false,
            errors:[]
            }
        },
        methods:{
            login(email,password){
				const body = {
					'email': email,
					'password': password
				};
				axios.post('http://localhost:5000/login?include_auth_token',body)
				.then((res) => {
                    this.errors=[]
					store.commit('login');
                    store.commit('update_token', res.data.response.user.authentication_token)
                    const config = {
                        headers:{
                        'Content-Type': 'application/json',
                        'Authentication-Token': store.state.auth_token
					}}
                    axios.post('http://localhost:5000/user',body,config)
                    .then((res) =>{
                        store.commit('update_user',{...res.data})
                        console.log("success",store.state.user)
                    })
                    .catch((rej)=>{
                        console.log("failed",rej)
                    })
                    router.push('Tickets')
				})
                .catch((rej) =>{
                    this.errors = rej.response.data.response.errors
                })
            }
        }
    }
</script>