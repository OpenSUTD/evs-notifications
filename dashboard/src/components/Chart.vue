<template>
	<div id="chart">
		<canvas id="timeSeries"></canvas>
		<canvas id="usagePie"></canvas>
	</div>
</template>

<script>
import Chart from 'chart.js';
import { timeSeries } from './plots.js';

export default {
  name: 'Chart',

  methods: {
  	plot(balances) {
  		let dates = balances.map(t => t[0]);
  		let amounts = balances.map(t => t[1]);

  		let timeSeriesChart = timeSeries('timeSeries', dates, amounts);
  	},
  },

  mounted() {
  	fetch('http://54.255.186.25:8000/balance/20000173')
  	.then(response => response.json())
  	.then(json => this.plot(json));
  },
}
</script>

<style scoped>
</style>