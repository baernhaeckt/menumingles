.PHONY: help install dev test lint format clean docker-build docker-run docker-compose-up docker-compose-down

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install dependencies
	poetry install

dev: ## Run development server
	poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test: ## Run tests
	poetry run pytest

lint: ## Run linting
	poetry run flake8 app tests
	poetry run mypy app

format: ## Format code
	poetry run black app tests
	poetry run isort app tests

clean: ## Clean up cache files
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +

docker-build: ## Build Docker image
	docker build -t menu-minglers .

docker-run: ## Run Docker container
	docker run -p 8000:8000 menu-minglers

docker-compose-up: ## Start services with docker-compose
	docker-compose up -d

docker-compose-down: ## Stop services with docker-compose
	docker-compose down

docker-compose-logs: ## Show docker-compose logs
	docker-compose logs -f

all: install format lint test ## Run all checks (install, format, lint, test)
