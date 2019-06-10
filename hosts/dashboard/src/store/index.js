import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

const serverHost = 'https://gabrielwong159.pythonanywhere.com';

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
      let url = `${serverHost}/balance`;

      let headers = { 'Content-Type': 'application/json' };
      let body = JSON.stringify({ username, password });

      return fetch(url, { method: 'POST', headers, body })
      .then(response => {
        if (response.ok) return response.json();
        else throw new Error();
      })
      .then(json => { commit('loginSuccess', json) });
    },
    logout({ commit }) {
      commit('logout');
    },

    demo({ commit }) {
      let url = `${serverHost}/balance/demo`;
      return fetch(url)
      .then(response => response.json())
      .then(json => { commit('loginSuccess', json) });
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