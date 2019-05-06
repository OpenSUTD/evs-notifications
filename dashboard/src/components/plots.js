module.exports = {
	timeSeries: (elementId, dates, amounts) => {
		let ctx = document.getElementById(elementId).getContext('2d');
		let data = {
			labels: dates,
			datasets: [{
				label: 'Credit Balance',
				data: amounts,
			}],
		};
		let options = {
			maintainAspectRatio: false,
		};
		let timeSeries = new Chart(ctx, {
			type: 'line',
			data,
			options,
		});
		return timeSeries;
	},
};
