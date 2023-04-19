<template>
    <h5 class="row">{{ faq.question }}</h5>
    <p class="row">{{ faq.answer }}</p>
</template>

<script>
    import store from '@/store';
    import axios from 'axios';
    export default{
        name:"FAQBlock",
        props:{
            faq: {},
        },
        data(){
			return {
                faqcopy:{},
				current_user:{},
				auth_token: '',
				port:'http://localhost:5000/',
				headers: {},
                isEditing: false
			}
		},
        methods:{
            faq_edit(){
                this.faqcopy = {...this.faq}
                this.isEditing = !this.isEditing
            },
            save_changes(){
                const faq_id = this.faq.f_id
                const url = `faq/${faq_id}`
                const data = {'title':this.faqcopy.title,
                            'description': this.faqcopy.description}
                axios.put(this.port+url,data,{headers:this.headers})
                .then((res)=>{
                    console.log(res)
                    this.isEditing = false
                    this.$emit('faq_edited')
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