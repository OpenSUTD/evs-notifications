<template>
  <div id="balance">
    <h1 class="mb-3">Balance</h1>

    <v-btn-toggle mandatory id="toggleDates">
      <v-btn flat @click="plotAll()">All</v-btn>
      <v-btn flat @click="plotMonth()">Past Month</v-btn>
      <v-btn flat @click="plotWeek()">Past Week</v-btn>
    </v-btn-toggle>

    <v-container grid-list-md>
      <v-layout row>
        <v-flex xs12>
          <v-container elevation-2 class="chartContainer">
            <canvas id="balanceTimeSeries" />
          </v-container>
        </v-flex>
      </v-layout>
    </v-container>
  </div>
</template>

<script>
import { mapState } from 'vuex';
import {
  getPastWeekBalances,
  getPastMonthBalances,
  separateBalanceTuples,
} from './utils/data.js';
import { balanceTimeSeries } from './utils/plots.js';

export default {
  name: 'Balance',
  data() {
    return {
      charts: [],
    };
  },
  computed: {
    ...mapState(['balances']),
  },

  methods: {
    plot(balances) {
      this.destroyExistingCharts();

      let { dates, amounts } = separateBalanceTuples(balances);
      let timeSeriesChart = balanceTimeSeries('balanceTimeSeries', dates, amounts);
      this.charts = [timeSeriesChart];
    },

    plotAll() {
      this.plot(this.balances);
    },
    plotMonth() {
      let filteredBalances = getPastMonthBalances(this.balances);
      this.plot(filteredBalances);
    },
    plotWeek() {
      let filteredBalances = getPastWeekBalances(this.balances);
      this.plot(filteredBalances);
    },

    destroyExistingCharts() {
      // remove existing charts, otherwise new charts will simply overlap
      for (let chart of this.charts) chart.destroy();
    },
  },

  mounted() {
    // necessary to allow re-plotting when re-navigated to
    if (this.balances) this.plotAll();
  },

  watch: {
    balances: function() {
      // plot when updated with data from async fetch
      this.plotAll();
    },
  },
};
</script>

<style scoped>
#balance {
  height: 100%;
  width: 70%;
  margin: auto;
  padding-top: 60px;
}

.chartContainer {
  height: 100%;
  background-color: white;
}
</style>