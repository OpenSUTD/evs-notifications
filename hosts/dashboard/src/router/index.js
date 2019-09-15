import Vue from 'vue';
import Router from 'vue-router';
import Login from '@/views/Login';
import Balance from '@/views/Balance';
import Usage from '@/views/Usage';
import Topup from '@/views/Topup';
import Notifications from '@/views/Notifications';
import store from '../store';

Vue.use(Router);

function requireDeauth(to, from, next) {
  if (!store.getters.authenticated) next();
  else next(from.path);
}

function requireAuth(to, from, next) {
  if (store.getters.authenticated) next();
  else next('/login');
}

const router = new Router({
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: Login,
      beforeEnter: requireDeauth,
    },
    {
      path: '/balance',
      name: 'Balance',
      component: Balance,
      beforeEnter: requireAuth,
    },
    {
      path: '/usage',
      name: 'Usage',
      component: Usage,
      beforeEnter: requireAuth,
    },
    {
      path: '/topup',
      name: 'Topup',
      component: Topup,
      beforeEnter: requireAuth,
    },
    {
      path: '/notifications',
      name: 'Notifications',
      component: Notifications,
      beforeEnter: requireAuth,
    },
    {
      path: '*',
      redirect: '/login',
    },
  ],
});

export default router;