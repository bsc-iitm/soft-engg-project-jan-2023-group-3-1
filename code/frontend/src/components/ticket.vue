<template>
    <h4>{{ title }}</h4>
    <p> {{ desc }}</p>
</template>

<script>
    import store from '@/store';
	// import axios from 'axios'
    export default{
        name:"TicketBlock",
        props:{
            title: String,
            desc: String
        },
        data(){
			return {
				current_user:{},
				auth_token: '',
				port:'http://localhost:5000/',
				headers: {}
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