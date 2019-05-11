<template>
  <v-app id="app">
    <Chart :balances="balances" />
  </v-app>
</template>

<script>
import Chart from './components/Chart.vue';

export default {
  name: 'app',
  components: {
    Chart,
  },

  data() {
    return {
      balances: null,
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

  height: 100%;
}
</style>
