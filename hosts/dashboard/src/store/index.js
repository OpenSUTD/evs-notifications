import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    balances: null,
    authenticated: false,
  },

  getters: {
    authenticated: state => state.authenticated,
  },

  actions: {
    login({ commit }, { username, password }) {
      let serverHost = 'http://13.251.125.232:8000';
      let url = `${serverHost}/balance/${username}`;
      return fetch(url)
      .then(response => response.json())
      .then(json => { commit('loginSuccess', json) })
      .then(() => { console.log('fetch', url) });
    },
    logout({ commit }) {
      commit('logout');
    },
  },

  mutations: {
    loginSuccess(state, data) {
      state.balances = data;
      state.authenticated = true;
    },
    logout(state) {
      state.balances = null;
      state.authenticated = false;
    },
  },
});