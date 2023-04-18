<template>
    <div class="mb-3">
    <div class="row border d-flex align-items-center">
        <button @click="upvote()" type="button" class="col-1 btn">
            <i class="fa-solid fa-up-long"></i>
        </button>
        <h5 class="col-1 m-0">{{ticket.upvotes}}</h5>
        <p v-if="!isEditing" class="col m-0">{{ticket.title}}</p>
        <input v-else class="col m-0 " v-model="ticketcopy.title">
        <div class="col-1 text-end" @click="toggleDropdown">
            <i :class="{'fa-chevron-up': isOpen, 'fa-chevron-down': !isOpen}" class="fas fa-chevron-down"></i>
        </div>
    </div>
    <div class="row border d-flex align-items-center" v-if="isOpen" name="desc_dropdown">
        <p v-if="!isEditing" class="col w-75 text-start m-0">{{ticket.description}}</p>
        <input v-else class="col-1 w-75 text-start m-0 f" v-model="ticketcopy.description">
        <input v-if="isStaff" class="col-1 w-75 text-start m-0 f" v-model="ticketcopy.response">
        <div class="col w-25 text-end">
            <div>
                <button v-if="isEditing" @click="save_changes()" type="button" class="btn btn-outline-success">
                    <i class="fa-solid fa-check"></i>
                </button>
                <button v-if="!isEditing" @click="ticket_edit()" type="button" class="btn">
                    <i class="fa-solid fa-pen-to-square"></i>
                </button>
                <button v-if="isEditing" @click="ticket_edit()" type="button" class="btn btn-outline-danger">
                    <i class="fa-solid fa-xmark"></i>
                </button>
                <button v-if="isStaff" @click="answer_ticket()" type="button" class="btn">
                    <i class="fa-solid fa-paper-plane"></i>
                </button>
                <button v-if="isStaff" @click="ticket_delete()" type="button" class="col btn btn-outline-danger">
                    <i class="fa-regular fa-trash-can"></i>
                </button>
            </div>
        </div>
    </div>
    <div class="row d-flex align-items-center border">
        <p class="col-5 text-start m-0">{{ticket.last_modified}}</p>
        <p class="col text-start m-0">{{ticket.date_created}}</p>
        <div v-if="ticket.date_closed" class="col text-end">
            <i class="text-success fa-solid fa-check fa-2x"></i>
        </div>
        
    </div>
    </div>
</template>

<script>
    import store from '@/store';
    import axios from 'axios';
    export default{
        name:"TicketBlock",
        props:{
            ticket: {},
        },
        data(){
			return {
                ticketcopy:{},
				current_user:{},
				auth_token: '',
				port:'http://localhost:5000/',
				headers: {},
                isOpen: false,
                isEditing: false,
                isStaff: true
			}
		},
        methods:{
            toggleDropdown(){
                this.isOpen = !this.isOpen
            },
            ticket_edit(){
                this.ticketcopy = {...this.ticket}
                this.isEditing = !this.isEditing
            },
            save_changes(){
                const ticket_id = this.ticket.ticket_id
                const url = `ticket/${ticket_id}`
                const data = {'title':this.ticketcopy.title,
                            'description': this.ticketcopy.description}
                axios.put(this.port+url,data,{headers:this.headers})
                .then((res)=>{
                    console.log(res)
                    this.isEditing = false
                    this.$emit('ticket_edited')
                })
                .catch((rej)=>{
                    console.log(rej)
                })
            },
            answer_ticket(){
                const ticket_id = this.ticket.ticket_id
                const url = `tickets/${ticket_id}/answer`
                const data = {'title':this.ticketcopy.title,
                            'description': this.ticketcopy.description,
                            'response': this.ticketcopy.response}
                axios.post(this.port+url,data,{headers:this.headers})
                .then((res)=>{
                    console.log(res)
                    this.isEditing = false
                    this.$emit('ticket_edited')
                })
                .catch((rej)=>{
                    console.log(rej)
                })

            },
            upvote(){
                const url = "tickets/upvote"
                const data = {'title':this.ticketcopy.title,
                            'ticket_id': this.ticketcopy.ticket_id}
                axios.put(this.port+url,data,{headers:this.headers})
                .then((res)=>{
                    console.log(this.ticketcopy,res)
                    this.$emit('ticket_edited')
                })
                .catch((rej)=>{
                    console.log(rej)
                })

            }
        },
        created(){
            this.ticketcopy = { ...this.ticket}
        },
        async mounted() {
            this.current_user = store.state.user
            //this.isStaff = this.current_user.roles.includes('Support Staff')
            this.auth_token = store.state.auth_token
            this.headers = {
                'Content-Type': 'application/json',
                'Authentication-Token': this.auth_token
                }
		}
    }
</script>

<style>
    i {
        transition: transform 0.3s ease-in-out;
    }

    .fa-chevron-up {
        transform: rotate(-180deg);
    }
    textarea:focus, input:focus{
        outline: none;
    }
</style>