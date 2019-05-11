module.exports = {
	timeSeries: (elementId, dates, amounts) => {
		let ctx = document.getElementById(elementId).getContext('2d');
		let data = {
			labels: dates,
			datasets: [{
				label: 'Daily credit balance',
				data: amounts,
				backgroundColor: 'rgba(54, 162, 235, 0.3)',
			}],
		};
		let options = {
			scales: {
				xAxes: [{
					type: 'time',
					time: {
						unit: dates.length <= 40 ? 'day' : 'week',
						displayFormats: {
							week: 'D MMM YY',
							day: 'D MMM YY',
						},
					},
				}],
			},
		};
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
		let usagePie = new Chart(ctx, {
			type: 'pie',
			data,
			options: {
				maintainAspectRatio: false,
				title: {
					text: 'Number of days of air-con used',
					display: true,
				},
			},
		});
		return usagePie;
	},

	usageHist: (elementId, amounts) => {
		let usages = [];
		for (let i=1; i<amounts.length; i++) {
			let usage = amounts[i-1] - amounts[i];
			if (usage < 0) continue;  // signifies a top-up
			usage = Math.round(usage * 100) / 100;  // round to 2 d.p.
			usages.push(usage);
		}

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
				label: 'Daily usage amounts ($)',
				data: binCounts,
				backgroundColor: '#ffce56',
			}],
		};
		let usageHist = new Chart(ctx, {
			type: 'bar',
			data,
		});
		return usageHist;
	},
};
