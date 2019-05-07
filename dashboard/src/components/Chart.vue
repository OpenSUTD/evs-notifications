<template>
	<div id="chart">
		<v-container grid-list-md>
	    <v-layout row>
	    	<v-flex xs12>
		    	<v-container elevation-2>
						<canvas id="timeSeries"></canvas>
		    	</v-container>
		    </v-flex>
	    </v-layout>

	    <v-layout row>
	      <v-flex xs8>
	      	<v-container elevation-2>
	    			<canvas id="usageHist"></canvas>
					</v-container>
	      </v-flex>
	      <v-flex xs4>
	      	<v-container elevation-2>
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
  		balances: null,
  	};
  },

  methods: {
  	plot(dates, amounts) {
  		timeSeries('timeSeries', dates, amounts);
  		usagePie('usagePie', amounts);
  		usageHist('usageHist', amounts);
  	},
  },

  mounted() {
  	fetch('http://13.250.48.152:8000/balance/20000173')
  	.then(response => response.json())
  	.then(balances => {
  		let dates = balances.map(t => t[0]).map(date => Date.parse(date));
  		let amounts = balances.map(t => t[1]);

  		this.plot(dates, amounts);
  		this.balances = { dates, amounts };
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

.container {
	height: 100%;
}
</style>