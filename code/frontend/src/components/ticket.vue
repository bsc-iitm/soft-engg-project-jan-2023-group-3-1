<template>
    <h4>{{ title }}</h4>
    <p> {{ desc }}</p>
</template>

<script>
    export default{
        name:"TicketBlock",
        props:{
            title: String,
            desc: String
        }
    }
</script>