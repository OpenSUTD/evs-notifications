let Chart = require('chart.js');
let moment = require('moment');

function computeUsages(amounts) {
		let usages = [];
		for (let i=1; i<amounts.length; i++) {
			let usage = amounts[i-1] - amounts[i];
			if (usage < 0) continue;  // signifies a top-up
			usage = Math.round(usage * 100) / 100;  // round to 2 d.p.
			usages.push(usage);
		}
		return usages;
}

function timeSeriesOptions(title, label, timeUnit) {
	return {
		title: {
			text: title,
			display: true,
		},
		legend: {
			display: false,
		},
		scales: {
			xAxes: [{
				type: 'time',
				time: {
					unit: timeUnit,
					displayFormats: {
						week: 'D MMM YY',
						day: 'D MMM YY',
					},
				},
			}],
	    yAxes: [{
	      scaleLabel: {
	        display: true,
	        labelString: label,
	      },
	    }],
		},
		tooltips: {
			callbacks: {
				title: (tooltipItems, data) => {
					let item = tooltipItems[0];
					let date = Date.parse(item.xLabel);
					let formattedDate = moment(date).format('D MMM YY');
					return formattedDate;
				},
				label: (tooltipItem, data) => {
					let amt = tooltipItem.yLabel;
					return '$' + amt.toFixed(2);
				},
			},
		},
	};
}

module.exports = {
	balanceTimeSeries: (elementId, dates, amounts) => {
		let title = 'Credit balance history';
		let label = 'Credit balance ($)';
		let timeUnit = dates.length >= 32 ? 'week': 'day';

		let ctx = document.getElementById(elementId).getContext('2d');
		let data = {
			labels: dates,
			datasets: [{
				data: amounts,
				backgroundColor: 'rgba(54, 162, 235, 0.3)',
			}],
		};
		let options = timeSeriesOptions(title, label, timeUnit);
		let timeSeries = new Chart(ctx, {
			type: 'line',
			data,
			options,
		});
		return timeSeries;
	},

	usageTimeSeries: (elementId, dates, amounts) => {
		let usages = computeUsages(amounts);

		let title = 'Usage history';
		let label = 'Usage amount ($)';
		let timeUnit = dates.length >= 32 ? 'week': 'day';

		let ctx = document.getElementById(elementId).getContext('2d');
		let data = {
			labels: dates,
			datasets: [{
				data: usages,
				backgroundColor: 'rgba(54, 162, 235, 0.3)',
			}],
		};
		let options = timeSeriesOptions(title, label, timeUnit);
		let timeSeries = new Chart(ctx, {
			type: 'line',
			data,
			options,
		});
		return timeSeries;
	},

	usagePie: (elementId, amounts) => {
		let used = 0;
		for (let i=1; i<amounts.length; i++) {
			if (amounts[i] !== amounts[i-1]) used++;
		}
		let N = amounts.length - 1;
		let counts = [used, N - used];

		let ctx = document.getElementById(elementId).getContext('2d');
		let data = {
			labels: ['Used', 'Not used'],
			datasets: [{
				data: counts,
				backgroundColor: ['#ff6384', '#36a2eb'],
			}],
		};
		let options = {
			maintainAspectRatio: false,
			title: {
				text: 'Number of days of air-con used',
				display: true,
			},
		};
		let usagePie = new Chart(ctx, {
			type: 'pie',
			data,
			options,
		});
		return usagePie;
	},

	usageHist: (elementId, amounts) => {
		let usages = computeUsages(amounts);

		let nbins = 10;
		let binCounts = Array(nbins+1).fill(0);  // bins are multiples of 0.1
		for (let i=0; i<usages.length; i++) {
			let usage = usages[i];
			let binIndex = Math.round(usage / 0.1);
			if (binIndex > nbins) { binCounts[nbins]++; }
			else binCounts[binIndex]++;
		}

		let labels = [];
		for (let i=0; i<nbins; i++) labels.push((i * 0.1).toFixed(1));
		labels.push(`≥ ${(nbins*0.1).toFixed(1)}`);

		// remove instances of 0 usage
		labels = labels.slice(1);
		binCounts = binCounts.slice(1);

		let ctx = document.getElementById(elementId).getContext('2d');
		let data = {
			labels,
			datasets: [{
				data: binCounts,
				backgroundColor: '#ffce56',
			}],
		};
		let options = {
			title: {
				text: 'Amount of credit used per day',
				display: true,
			},
			legend: {
				display: false,
			},
			scales: {
				xAxes: [{
					scaleLabel: {
						display: true,
						labelString: 'Daily usage amount ($)',
					},
				}],
		    yAxes: [{
		      scaleLabel: {
		        display: true,
		        labelString: 'Counts',
		      },
		    }],
		  },
			tooltips: {
				callbacks: {
					title: (tooltipItems, data) => {
						let item = tooltipItems[0];
						return item.yLabel;
					},
					label: (tooltipItem, data) => {
						let label = tooltipItem.xLabel;
						let heading = data.datasets[0].label;
						return `${heading}: ${label}`;
					}
				},
			},
		};
		let usageHist = new Chart(ctx, {
			type: 'bar',
			data,
			options,
		});
		return usageHist;
	},
};
