<template>
  <v-app id="app">
    <NavigationDrawer
      :pages="pages"
      @changeDisplay="flag => { display = flag }" />

    <Usage v-if="display === flags.usage" :balances="balances" />
    <Topup v-if="display === flags.topup" />
    <Notifications v-if="display === flags.notifications" />
  </v-app>
</template>

<script>
import NavigationDrawer from './components/NavigationDrawer.vue';
import Usage from './components/Usage.vue';
import Topup from './components/Topup.vue';
import Notifications from './components/Notifications.vue';

let flags = {
  usage: 'usage',
  topup: 'topup',
  notifications: 'notifications',
};
let pages = [
  {
    title: 'Usage History',
    icon: 'timeline',
    flag: flags.usage,
  },
  {
    title: 'Topup Statistics',
    icon: 'autorenew',
    flag: flags.topup,
  },
  {
    title: 'Notifications',
    icon: 'announcement',
    flag: flags.notifications,
  },
];

export default {
  name: 'app',
  components: {
    NavigationDrawer,
    Usage,
    Topup,
    Notifications,
  },

  data() {
    return {
      balances: null,
      display: 'usage',
      flags,
      pages,
    };
  },

  created() {
    let serverHost = 'http://13.250.48.152:8000';
    let accountId = '20000173';
    let url = `${serverHost}/balance/${accountId}`;
    fetch(url)
    .then(response => response.json())
    .then(json => { this.balances = json });
  }
}
</script>

<style>
html, body {
  height: 100%;
  overflow: auto;
}

#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;

  display: flex;
}

#app > div {
  /* div wrapped by v-app */
  flex-direction: row;
  height: 100%;
}
</style>
