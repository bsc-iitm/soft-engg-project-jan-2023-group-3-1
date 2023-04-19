import { createStore } from 'vuex'
import VuexPersist from 'vuex-persist'
import axios from 'axios'

const vuexPersist = new VuexPersist({
  key: 'user',
  storage: window.sessionStorage,   
  reducer: (state) => ({ logged_in: state.logged_in, auth_token: state.auth_token, user:state.user}) 
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
        const path = 'http://localhost:5000//logout'
        axios.get(path)
        .then((res)=>{
          console.log(state)
          state.logged_in = false
          console.log(res)
          console.log('hello')
        })
        .catch((rej)=>{console.log(rej)})
    },
    update_token(state, token){
      state.auth_token = token
    },
    update_user(state, user){
      state.user = {...user}
    }
  },
  plugins: [vuexPersist.plugin]
});