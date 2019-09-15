<template>
  <v-navigation-drawer
    :mini-variant="mini"
    permanent
    touchless>
    <v-toolbar flat>
      <v-list>
        <v-list-tile>
          <v-list-tile-action>
            <v-icon>dashboard</v-icon>
          </v-list-tile-action>
          <v-list-tile-content>
            <v-list-tile-title class="title">
              EVS Dashboard
            </v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>
      </v-list>
    </v-toolbar>

    <v-divider />

    <v-list class="pt-0">
      <v-list-tile v-ripple v-for="(page, index) in pages"
        :key="index"
        :to="page.path"
      >
        <v-list-tile-action>
          <v-icon>{{ page.icon }}</v-icon>
        </v-list-tile-action>
        <v-list-tile-content>
          <v-list-tile-title>{{ page.title }}</v-list-tile-title>
        </v-list-tile-content>
      </v-list-tile>

      <v-divider />
      <v-list-tile v-ripple @click="logout">
        <v-list-tile-action>
          <v-icon>exit_to_app</v-icon>
        </v-list-tile-action>
        <v-list-tile-content>
          <v-list-tile-title>Logout</v-list-tile-title>
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

  computed: {
    mini() {
      let isMobile = this.$vuetify.breakpoint.smAndDown;
      return isMobile;
    },
  },

  methods: {
    logout() {
      this.$store.dispatch('logout');
      this.$router.push('/login');
    },
  },
};
</script>

<style scoped>
.title {
  line-height: 24px !important;
}
</style>