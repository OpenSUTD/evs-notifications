#!/bin/bash
echo "\copy account to 'account.csv' csv header" | PGPASSWORD=docker psql -h localhost -U postgres -d evs
echo "\copy balance to 'balance.csv' csv header" | PGPASSWORD=docker psql -h localhost -U postgres -d evs
echo "\copy notification to 'notification.csv' csv header" | PGPASSWORD=docker psql -h localhost -U postgres -d evs
echo "\copy subscription to 'subscription.csv' csv header" | PGPASSWORD=docker psql -h localhost -U postgres -d evs
