<template>
    <div class="border row">
        <div class="col">
            <div class="row d-flex">
                <input v-if="isEditing" v-model="faqcopy.question">
                <h5 v-else>Q. {{ faq.question }}</h5>
            </div>
            <div class="row">
                <input v-if="isEditing" v-model="faqcopy.answer">
                <p v-else class="col">ans. {{ faq.answer }}</p>
            </div>
        </div>
        
        <div v-if="current_user.role == 'Admin'" class="col-1 w-25 text-end m-0">
            <div v-if="isEditing" class="row">
                <button @click="save_changes()" type="button" class="btn btn-outline-success">
                    <i class="fa-solid fa-check"></i>
                </button>
                <button @click="faq_edit()" type="button" class="btn btn-outline-danger">
                    <i class="fa-solid fa-xmark"></i>
                </button>
            </div>
            <div v-else>
                <button @click="faq_edit()" type="button" class="btn">
                    <i class="fa-solid fa-pen-to-square"></i>
                </button>
                <button @click="faq_delete()" type="button" class="col btn btn-outline-danger">
                    <i class="fa-regular fa-trash-can"></i>
                </button>
            </div>
        </div>
    </div>
    
</template>

<script>
    import store from '@/store';
    import axios from 'axios';
    export default{
        name:"FAQBlock",
        props:{
            faq: {},
        },
        emits:{
            faq_edited: null,
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
                const url = `faqs/${faq_id}`
                const data = {'question':this.faqcopy.question,
                            'answer': this.faqcopy.answer}
                axios.put(this.port+url,data,{headers:this.headers})
                .then((res)=>{
                    console.log(res)
                    this.isEditing = false
                    this.$emit('faq_edited')
                })
                .catch((rej)=>{
                    console.log(rej)
                })
            },
            faq_delete(){
                const f_id = this.faq.f_id
                const url = `faqs/${f_id}`
                axios.delete(this.port+url,{headers:this.headers})
                .then((res)=>{
                    console.log(res)
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