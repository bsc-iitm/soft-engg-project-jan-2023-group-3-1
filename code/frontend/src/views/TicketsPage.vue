<template>
	<div>
		<h1>This is the tickets page</h1>
	</div>
	<div>
		<ticket title="Ticket1" desc="random desc">

		</ticket>
	</div>
</template>

<script>
	import ticket from "../components/ticket.vue";
	export default {
		name: "TicketsPage",
		components: {
			ticket
		}
	}
</script>