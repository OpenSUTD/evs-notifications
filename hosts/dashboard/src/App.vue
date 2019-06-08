<template>
  <v-app id="app">
    <router-view/>
  </v-app>
</template>

<script>
export default {
  name: 'app',
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
