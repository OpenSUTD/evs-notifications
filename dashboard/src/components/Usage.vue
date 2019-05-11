<template>
	<div id="usage">
		<v-btn-toggle mandatory id="toggleDates">
			<v-btn flat @click="plotAll()">All</v-btn>
			<v-btn flat @click="plotMonth()">Past Month</v-btn>
			<v-btn flat @click="plotWeek()">Past Week</v-btn>
		</v-btn-toggle>

		<v-container grid-list-md>
	    <v-layout row>
	    	<v-flex xs12>
		    	<v-container elevation-2 class="chartContainer">
						<canvas id="timeSeries"></canvas>
		    	</v-container>
		    </v-flex>
	    </v-layout>

	    <v-layout row>
	      <v-flex xs8>
	      	<v-container elevation-2 class="chartContainer">
	    			<canvas id="usageHist"></canvas>
					</v-container>
	      </v-flex>
	      <v-flex xs4>
	      	<v-container elevation-2 class="chartContainer">
						<canvas id="usagePie"></canvas>
					</v-container>
	      </v-flex>
	    </v-layout>
	  </v-container>
	</div>
</template>

<script>
import Chart from 'chart.js';
import { timeSeries, usagePie, usageHist } from './usage/plots.js';

export default {
  name: 'Usage',
  props: ['balances'],
  data() {
  	return {
  		charts: [],
  	};
  },

  methods: {
  	plot(balances) {
  		this.destroyExistingCharts();

  		let { dates, amounts } = this.separateBalanceTuples(balances);
  		let timeSeriesChart = timeSeries('timeSeries', dates, amounts);
  		let usagePieChart = usagePie('usagePie', amounts);
  		let usageHistChart = usageHist('usageHist', amounts);

  		this.charts = [
  			timeSeriesChart,
  			usagePieChart,
  			usageHistChart,
  		];
  	},

  	plotAll() {
  		this.plot(this.balances);
  	},
  	plotMonth() {
  		let filterDate = new Date();
  		filterDate.setHours(0, 0, 0, 0);  // prevent comparing against current time of day
  		filterDate.setMonth(filterDate.getMonth() - 1);

  		let filteredBalances = this.balances.filter(t => Date.parse(t[0]) >= filterDate);
  		this.plot(filteredBalances);
  	},
  	plotWeek() {
  		let filterDate = new Date();
  		filterDate.setHours(0, 0, 0, 0);
  		filterDate.setDate(filterDate.getDate() - 7);

  		let filteredBalances = this.balances.filter(t => Date.parse(t[0]) >= filterDate);
  		this.plot(filteredBalances);
  	},

    separateBalanceTuples(balances) {
      let dates = balances.map(t => t[0]).map(date => Date.parse(date));
      let amounts = balances.map(t => t[1]);
      return { dates, amounts };
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
}
</script>

<style scoped>
#usage {
	height: 100%;
	margin: auto;
  margin-top: 60px;
}

.chartContainer {
	height: 100%;
}
</style>