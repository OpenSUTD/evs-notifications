include .env

.DEFAULT_GOAL:=help

.PHONY: up db-shell certbot-init certbot-renew help

up:  ## Start necessary services for app (certbot not included)
	docker compose up -d nginx telebot grafana

db-shell:  ## Create Postgres shell
	docker compose exec db psql -U ${POSTGRES_USER} -d ${POSTGRES_DB}

certbot-init:  ## Retrieve initial HTTPS certificates
	docker compose run --rm certbot certonly --webroot --webroot-path /var/www/certbot/ -d api.evs.gabrielwong.dev -v

certbot-renew:  ## Renew HTTPS certificates
	docker compose run --rm certbot renew

help:  ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
