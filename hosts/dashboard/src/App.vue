<template>
  <v-app id="app">
    <NavigationDrawer v-if="showNav"/>
    <router-view />
  </v-app>
</template>

<script>
import NavigationDrawer from '@/components/NavigationDrawer.vue';

export default {
  name: 'app',
  components: {
    NavigationDrawer,
  },
  computed: {
    showNav() {
      return this.$route.path !== '/login';
    },
  },
};
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
}

.application--wrap {
  display: flex;
  flex-direction: row;
}
</style>
