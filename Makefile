.PHONY: help build run stop test admin local_confmap prod_confmap

help:
	@echo "Available targets:"
	@echo "  help    - Show this help message."
	@echo "  build   - Build the docker image."
	@echo "  run     - Run the docker container."
	@echo "  deploy  - Deploy the docker container."
	@echo "  stop    - Stop the docker container."
	@echo "  test    - Run the tests."
	@echo "  migrations - Create migrations."
	@echo "  migrate - Migrate"
	@echo "  k8s    - Deploy to k8s"
	@echo "  local_confmap - Make Kubernetes config maps for local stage"
	@echo "  prod_confmap - Make Kubernetes config maps for production stage"


build:
	docker compose build

run:
ifeq ($(DETACHED),true)
	docker compose up -d
else
	docker compose up
endif

deploy:
	docker compose -f docker-compose.prod.yml up -d

stop:
	docker compose down

test:
	docker exec tsuna-streaming-backend pytest

migrations:
	docker exec tsuna-streaming-backend python manage.py makemigrations

migrate:
	docker exec tsuna-streaming-backend python manage.py migrate

k8s:
	kubectl apply -f kubernetes/postgres && kubectl apply -f kubernetes/redis && kubectl apply -f kubernetes/smtp4dev && kubectl apply -f kubernetes/backend && kubectl apply -f kubernetes/celery

local_confmap:
	kubectl create configmap tsuna-streaming-env --from-env-file=./backend/.env.local && kubectl create configmap tsuna-streaming-env-file --from-file=.env=./backend/.env.local && kubectl create configmap prometheus-config --from-file=prometheus.yml=./prometheus/config.yaml

prod_confmap:
	kubectl create configmap tsuna-streaming-env --from-env-file=./backend/.env.prod && kubectl create configmap tsuna-streaming-env-file --from-file=.env=./backend/.env.prod && kubectl create configmap prometheus-config --from-file=prometheus.yml=./prometheus/config.yaml