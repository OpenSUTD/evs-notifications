function filterBalancesByDate(balances, earliestDate) {
	let dateFilter = (t) => Date.parse(t[0]) >= earliestDate;
	return balances.filter(dateFilter);
}

module.exports = {
	getPastWeekBalances: (balances) => {
		let filterDate = new Date();
		filterDate.setHours(0, 0, 0, 0);
		filterDate.setDate(filterDate.getDate() - 7);
		return filterBalancesByDate(balances, filterDate);
	},

	getPastMonthBalances: (balances) => {
		let filterDate = new Date();
		filterDate.setHours(0, 0, 0, 0);
		filterDate.setMonth(filterDate.getMonth() - 1);
		return filterBalancesByDate(balances, filterDate);
	},
	
	separateBalanceTuples: (balances) => {
		let dates = balances.map(t => t[0]).map(date => Date.parse(date));
		let amounts = balances.map(t => t[1]);
		return { dates, amounts };
	},
};