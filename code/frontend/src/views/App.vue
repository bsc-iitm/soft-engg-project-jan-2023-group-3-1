<template>
  <div id="app">
    <header>
      <nav>
        <ul>
          <li><router-link to="/">Home</router-link></li>
          <li v-if="loggedIn"><router-link to="/faq">FAQ</router-link></li>
          <li v-if="loggedIn"><a href="#" @click="logout">Logout</a></li>
          <li v-else><router-link to="/login">Login</router-link></li>
          <li v-else><router-link to="/signup">Sign Up</router-link></li>
        </ul>
      </nav>
    </header>
    <main>
      <router-view />
    </main>
    <footer>
      <p>&copy; 2023 My Awesome Company</p>
    </footer>
  </div>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  computed: {
    ...mapGetters(["loggedIn"])
  },
  methods: {
    logout() {
      this.$store.dispatch("logout");
      this.$router.push("/");
    }
  }
};
</script>

<style>
/* Add your styles here */
</style>
