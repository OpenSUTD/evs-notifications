<template>
	<div id="chart">
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
import { timeSeries, usagePie, usageHist } from './plots.js';

export default {
  name: 'Chart',
  data() {
  	return {
  		balances: [],
  		charts: [],
  	};
  },

  methods: {
  	separateBalanceTuples(balances) {
  		let dates = balances.map(t => t[0]).map(date => Date.parse(date));
  		let amounts = balances.map(t => t[1]);
  		return { dates, amounts };
  	},
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
  	destroyExistingCharts() {
  		// remove existing charts, otherwise new charts will simply overlap
  		for (let chart of this.charts) chart.destroy();
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
  },

  mounted() {
  	fetch('http://13.250.48.152:8000/balance/20000173')
  	.then(response => response.json())
  	.then(balances => {
  		this.plot(balances);
  		this.balances = balances;
  	});
  },
}
</script>

<style scoped>
#chart {
	height: 100%;
	width: 50%;
	margin: auto;
}

#toggleDates {
	margin-top: 32px;
}

.chartContainer {
	height: 100%;
}
</style>