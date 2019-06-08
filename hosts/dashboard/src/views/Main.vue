<template>
  <div id="main">
    <NavigationDrawer
      :pages="pages"
      @changeDisplay="flag => { display = flag }" />

    <Balance v-if="display === flags.balance" :balances="balances" />
    <Usage v-if="display === flags.usage" :balances="balances" />
    <Topup v-if="display === flags.topup" :balances="balances" />
    <Notifications v-if="display === flags.notifications" />
  </div>
</template>

<script>
import NavigationDrawer from '@/components/NavigationDrawer.vue';
import Balance from '@/components/Balance.vue';
import Usage from '@/components/Usage.vue';
import Topup from '@/components/Topup.vue';
import Notifications from '@/components/Notifications.vue';

let flags = {
  balance: 'balance',
  usage: 'usage',
  topup: 'topup',
  notifications: 'notifications',
};

let pages = [
  {
    title: 'Daily Balance',
    icon: 'credit_card',
    flag: flags.balance,
  },
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
  name: 'Main',
  components: {
    NavigationDrawer,
    Balance,
    Usage,
    Topup,
    Notifications,
  },

  data() {
    return {
      balances: null,
      display: flags.balance,
      flags,
      pages,
    };
  },

  created() {
    let serverHost = 'http://13.251.125.232:8000';
    let accountId = '20000173';
    let url = `${serverHost}/balance/${accountId}`;
    fetch(url)
    .then(response => response.json())
    .then(json => { this.balances = json });
  }
};
</script>

<style scoped>
#main {
  display: flex;
  flex-direction: row;
  height: 100%;
}
</style>