<template>
  <div id="balance">
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
import {
  getPastWeekBalances,
  getPastMonthBalances,
  separateBalanceTuples,
} from './utils/data.js';
import { balanceTimeSeries } from './utils/plots.js';

export default {
  name: 'Balance',
  props: ['balances'],
  data() {
    return {
      charts: [],
    };
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
    // from navigation drawer
    if (this.balances) this.plotAll();
  },

  watch: {
    balances: function(newBalances, oldBalances) {
      // plot when updated with data from async fetch
      this.balances = newBalances;
      this.plotAll();
    },
  },
};
</script>

<style scoped>
#balance {
  height: 100%;
  width: 100%;
  padding-top: 60px;
}

.chartContainer {
  height: 100%;
}
</style>