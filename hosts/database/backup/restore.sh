#!/bin/bash
echo "\copy account from 'account.csv' csv header" | PGPASSWORD=docker psql -h localhost -U postgres -d evs
echo "\copy balance from 'balance.csv' csv header" | PGPASSWORD=docker psql -h localhost -U postgres -d evs
echo "\copy notification from 'notification.csv' csv header" | PGPASSWORD=docker psql -h localhost -U postgres -d evs
echo "\copy subscription from 'subscription.csv' csv header" | PGPASSWORD=docker psql -h localhost -U postgres -d evs
