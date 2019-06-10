<template>
  <div id="topup">
    <h1 class="mb-3">Topup</h1>

    <v-data-table id="table" class="elevation-1"
      :headers="headers"
      :items="topups">
      <template v-slot:items="props">
        <td class="text-xs-left"
          @click="dateFormat = !dateFormat">
          {{ formatDate(props.item.date) }}
        </td>
        <td class="text-xs-right">{{ props.item.estAmt }}</td>
        <td class="text-xs-right">{{ props.item.daysSinceTopup }}</td>
        <td class="text-xs-right">{{ props.item.estDailyAvg }}</td>
      </template>
    </v-data-table>
  </div>
</template>

<script>
import { mapState } from 'vuex';
import moment from 'moment';
import { separateBalanceTuples } from './utils/data.js';

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
          text: 'Estimated topup amount ($)',
          sortable: false,
          align: 'right',
        },
        {
          text: 'Days since last topup',
          sortable: false,
          align: 'right',
        },
        {
          text: 'Estimated daily average ($)',
          sortable: false,
          align: 'right',
        }
      ],
      dateFormat: true,
    };
  },

  computed: {
    ...mapState(['balances']),
    topups: function() {
      let { dates, amounts } = separateBalanceTuples(this.balances);
      let topups = [];

      let lastTopupDate = null;
      for (let i=1; i<amounts.length; i++) {
        let diff = amounts[i] - amounts[i-1];
        if (diff <= 0) continue;  // not a topup

        let date = dates[i];
        let estAmt = Math.ceil(diff / 10) * 10;  // round up to nearest 10
        
        let daysSinceTopup = '-';
        if (lastTopupDate !== null) {
          daysSinceTopup = moment(date).diff(lastTopupDate, 'days');
        }
        lastTopupDate = moment(date);

        let estDailyAvg = 0;
        if (topups.length > 0) {
          let lastTopupAmt = topups[topups.length - 1].estAmt;
          estDailyAvg = lastTopupAmt / daysSinceTopup;
        }
        estDailyAvg = estDailyAvg !== 0 ? estDailyAvg.toFixed(2) : '-';

        topups.push({
          date,
          estAmt,
          daysSinceTopup,
          estDailyAvg,
        });
      }
      return topups;
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