<template>
    <div class="container mb-3 border">
        <div class="row">
            <h5> {{ ticket.user.username }}</h5>
        </div>
        <div class="row d-flex align-items-center border">
            <button @click="upvote()" type="button" :class="{'col-1 btn':!isUpvoted, 'col-1 btn text-success':isUpvoted}" class="col-1 btn">
                <i class="fa-solid fa-up-long"></i>
            </button>
            <h5 class="col-1 m-0">{{ticket.upvotes}}</h5>
            <p v-if="!isEditing" class="col m-0">{{ticket.title}}</p>
            <input v-else class="col m-0 " v-model="ticketcopy.title">
            <div class="col-1 text-end" @click="toggleDropdown">
                <i :class="{'fa-chevron-up': isOpen, 'fa-chevron-down': !isOpen}" class="fas fa-chevron-down"></i>
            </div>
        </div>
        <div class="row d-flex align-items-center border" v-if="isOpen" name="desc_dropdown">
            <p v-if="!isEditing" class="col w-75 text-start m-0">{{ticket.description}}</p>
            <input v-else class="col-1 w-75 text-start m-0 f" v-model="ticketcopy.description">
            <input v-if="isAnswering" class="col-1 w-75 text-start m-0 f" v-model="ticketcopy.response">
            <p v-else class="col-1 w-75 text-start m-0 f">{{ ticket.response }}</p>
            <div class="col w-25 text-end">
                <div v-if="current_user.id == ticket.user.id">
                    <div v-if="isEditing">
                        <button @click="save_changes()" type="button" class="btn btn-outline-success">
                            <i class="fa-solid fa-check"></i>
                        </button>
                        <button @click="ticket_edit()" type="button" class="btn btn-outline-danger">
                            <i class="fa-solid fa-xmark"></i>
                        </button>
                    </div>
                    <div v-else-if="ticket.status==='open'">
                        <button @click="ticket_edit()" type="button" class="btn">
                            <i class="fa-solid fa-pen-to-square"></i>
                        </button>
                    </div>
                </div>
                <div v-if="current_user.role == 'Support Staff'">
                    <div v-if="isAnswering">
                        <button @click="answer_ticket()" type="button" class="btn btn-outline-success">
                            <i class="fa-solid fa-check"></i>
                        </button>
                        <button @click="answering()" type="button" class="btn btn-outline-danger">
                            <i class="fa-solid fa-xmark"></i>
                        </button>
                    </div>
                    <div v-else>
                        <button @click="answering()" type="button" class="btn">
                            <i class="fa-solid fa-paper-plane"></i>
                        </button>
                        <button @click="ticket_delete()" type="button" class="col btn btn-outline-danger">
                            <i class="fa-regular fa-trash-can"></i>
                        </button>
                    </div>
                </div>
            </div>
        </div>
        <div class="row d-flex align-items-center">
            <p class="col-4 text-start m-0">Last modified {{time_to_text(ticket.last_modified)}}</p>
            <p class="col text-start m-0">Created {{time_to_text(ticket.date_created)}}</p>
            <p v-if="ticket.status == 'closed'" class="col text-start m-0"> Closed {{ time_to_text(ticket.date_closed) }}</p>
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
                isUpvoted: false,
                isAnswering: false,
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
            answering(){
                this.isAnswering = !this.isAnswering
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
            ticket_delete(){
                const ticket_id = this.ticket.ticket_id
                const url = `ticket/${ticket_id}`
                axios.delete(this.port+url,{headers:this.headers})
                .then((res)=>{
                    console.log(res)
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
                    if(res.data == 'post upvoted successfully'){
                        this.isUpvoted = true
                    }
                    else this.isUpvoted = false
                    this.$emit('ticket_edited')
                })
                .catch((rej)=>{
                    console.log(rej)
                })

            },
            time_to_text(time){
                var last_modified = new Date(time);
                var diff = new Date(this.present_datetime) - last_modified
                var seconds = diff/1000
                var minutes = seconds/60
                var hours = minutes/60
                var days = hours/24
                var weeks = days/7
                var months = weeks/30
                var years = months/12

                if(years > 1){
                    return Math.floor(years) + " years ago"
                }
                if(months > 1){
                    return Math.floor(months) + " months ago"
                }
                if(weeks > 1){
                    return Math.floor(weeks) + " weeks ago"
                }
                if(days > 1){
                    return  Math.floor(days) + " days ago"
                }
                if(hours > 1){
                    return Math.floor(hours) + " hours ago"
                }
                if(minutes > 1){
                    return Math.floor(minutes) + " minutes ago"
                }
                return "just now"
            }
        },
        computed:{
            present_datetime(){
                var curr = new Date()
                return curr.getFullYear()+'-'+(curr.getMonth()<9?'0':'')+(curr.getMonth()+1)+'-'+(curr.getDate()<10?'0':'')+curr.getDate()+'T'+(curr.getHours()<10?'0':'')+curr.getHours()+':'+(curr.getMinutes()<10?'0':'')+curr.getMinutes()
            }
        },
        created(){
            this.ticketcopy = { ...this.ticket}
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