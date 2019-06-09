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
      <v-list-tile v-ripple v-for="page in pages" :to="page.path">
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
let pages = [
  {
    title: 'Daily Balance',
    icon: 'credit_card',
    path: '/balance',
  },
  {
    title: 'Usage History',
    icon: 'timeline',
    path: '/usage',
  },
  {
    title: 'Topup Statistics',
    icon: 'autorenew',
    path: '/topup',
  },
  {
    title: 'Notifications',
    icon: 'announcement',
    path: '/notifications',
  },
];

export default {
	name: 'NavigationDrawer',
  data() {
    return {
      pages,
    };
  },
};
</script>

<style scoped>
</style>