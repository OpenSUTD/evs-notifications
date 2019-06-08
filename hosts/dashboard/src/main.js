import Vue from 'vue';
import Vuetify from 'vuetify';
import 'vuetify/dist/vuetify.min.css';
import App from './App.vue';
import router from './router';
import store from './store';

Vue.use(Vuetify);
Vue.config.productionTip = false;

new Vue({
  render: function (h) { return h(App) },
  router,
  store,
}).$mount('#app');
