<template>
  <v-app id="app">
    <!-- disable "height: 100%" style -->
    <v-navigation-drawer permanent height>
      <v-toolbar flat>
        <v-list>
          <v-list-tile>
            <v-list-tile-action>
              <v-icon>dashboard</v-icon>
            </v-list-tile-action>
            <v-list-tile-title class="title">
              EVS Dashboard
            </v-list-tile-title>
          </v-list-tile>
        </v-list>
      </v-toolbar>

      <v-divider />

      <v-list class="pt-0">
        <v-list-tile v-ripple @click="display = 'usage'">
          <v-list-tile-action>
            <v-icon>timeline</v-icon>
          </v-list-tile-action>
          <v-list-tile-content>
            <v-list-tile-title>Usage History</v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>

        <v-list-tile v-ripple @click="display = 'topup'">
          <v-list-tile-action>
            <v-icon>autorenew</v-icon>
          </v-list-tile-action>
          <v-list-tile-content>
            <v-list-tile-title>Topup Statistics</v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>

        <v-list-tile v-ripple @click="display = 'notifications'">
          <v-list-tile-action>
            <v-icon>announcement</v-icon>
          </v-list-tile-action>
          <v-list-tile-content>
            <v-list-tile-title>Notifications</v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>
      </v-list>
    </v-navigation-drawer>

    <Usage v-if="display === 'usage'" :balances="balances" />
  </v-app>
</template>

<script>
import Usage from './components/Usage.vue';

export default {
  name: 'app',
  components: {
    Usage,
  },

  data() {
    return {
      balances: null,
      display: 'usage',
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
