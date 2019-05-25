<template>
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
      <v-list-tile v-ripple v-for="page in pages"
        @click="$emit('changeDisplay', page.flag)">
        <v-list-tile-action>
          <v-icon>{{ page.icon }}</v-icon>
        </v-list-tile-action>
        <v-list-tile-content>
          <v-list-tile-title>{{ page.title }}</v-list-tile-title>
        </v-list-tile-content>
      </v-list-tile>
    </v-list>
  </v-navigation-drawer>
</template>

<script>
export default {
	name: 'NavigationDrawer',
	props: ['pages'],
};
</script>

<style scoped>
</style>