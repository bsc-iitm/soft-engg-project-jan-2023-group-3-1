import { createStore } from 'vuex'
import VuexPersist from 'vuex-persist'

const vuexPersist = new VuexPersist({
  key: 'user',
  storage: window.sessionStorage,   
  reducer: (state) => ({ logged_in: state.logged_in, auth_token: state.auth_token }) 
});

export default createStore({
  state () {
    return {
      logged_in: false,
      auth_token:'',
      user:{},
    }
  },
  mutations: {
    login(state){
        state.logged_in = true
    },
    logout(state){
        state.logged_in = false
    },
    update_token(state, token){
      state.auth_token = token
    },
    update_user(state, user){
      state.user = user
    }
  },
  plugins: [vuexPersist.plugin]
});