.PHONY: help install test lint format run docker-build docker-up docker-down k8s-deploy k8s-delete clean

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install dependencies
	pip install -r requirements.txt

install-dev: ## Install development dependencies
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

test: ## Run tests
	pytest tests/ -v --cov=src --cov-report=term-missing

test-watch: ## Run tests in watch mode
	pytest-watch tests/

lint: ## Run linters
	ruff check src/ tests/
	mypy src/

format: ## Format code
	ruff format src/ tests/
	black src/ tests/

run: ## Run the server
	python -m src.main

run-dev: ## Run the server in development mode
	DEBUG=true python -m src.main

docker-build: ## Build Docker image
	docker build -t mcp-server:latest .

docker-up: ## Start Docker Compose services
	docker-compose up -d

docker-down: ## Stop Docker Compose services
	docker-compose down

docker-logs: ## View Docker logs
	docker-compose logs -f mcp-server

k8s-deploy: ## Deploy to Kubernetes
	kubectl apply -f k8s/configmap.yaml
	kubectl apply -f k8s/deployment.yaml

k8s-delete: ## Delete Kubernetes resources
	kubectl delete -f k8s/

clean: ## Clean up generated files
	find . -type d -name __pycache__ -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf dist/
	rm -rf build/
	rm -rf *.egg-info

