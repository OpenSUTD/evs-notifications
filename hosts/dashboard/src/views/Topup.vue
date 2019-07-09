<template>
  <div id="topup">
    <h1 class="mb-3">Topup</h1>

    <v-data-table id="table" class="elevation-1"
      :headers="headers"
      :items="tableItems">
      <template v-slot:items="props">
        <td class="text-xs-left"
          @click="dateFormat = !dateFormat">
          {{ formatDate(props.item.date) }}
        </td>
        <td class="text-xs-right">{{ props.item.amount.toFixed(2) }}</td>
        <td class="text-xs-right">{{ props.item.daysSinceTopup }}</td>
        <td class="text-xs-right">{{ props.item.dailyAvg.toFixed(2) }}</td>
      </template>
    </v-data-table>
  </div>
</template>

<script>
import { mapState } from 'vuex';
import moment from 'moment';

export default {
  name: 'Topup',
  data() {
    return {
      headers: [
        {
          text: 'Date of topup',
          sortable: false,
        },
        { 
          text: 'Topup amount ($)',
          sortable: false,
          align: 'right',
        },
        {
          text: 'Days since last topup',
          sortable: false,
          align: 'right',
        },
        {
          text: 'Daily average ($)',
          sortable: false,
          align: 'right',
        }
      ],
      dateFormat: true,
    };
  },

  computed: {
    ...mapState(['transactions']),
    tableItems() {
      let transactions = this.transactions;
      let items = [];
      for (let i=0; i<transactions.length-1; i++) {
        let currDate = Date.parse(transactions[i].date);
        let prevDate = Date.parse(transactions[i+1].date);
        let daysSinceTopup = moment(currDate).diff(prevDate, 'days');

        let dailyAvg = transactions[i+1].amount / daysSinceTopup;

        items.push({
          date: transactions[i].date,
          amount: transactions[i].amount,
          daysSinceTopup,
          dailyAvg,
        });
      }
      return items;
    },
  },

  methods: {
    formatDate(date) {
      return moment(date).format(this.dateFormat ? 'DD MMM YYYY' : 'DD-MM-YYYY');
    },
  },
};
</script>

<style scoped>
#topup {
  height: 100%;
  width: 70%;
  margin: auto;
  padding-top: 60px;
}
</style>