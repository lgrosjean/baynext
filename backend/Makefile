# Backend development commands

.PHONY: help install db-create db-drop db-reset seed seed-fresh seed-clear seed-reset test lint

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	uv sync

# Database schema commands
db-create: ## Create database tables
	uv run scripts/cli.py db create

db-drop: ## Drop all database tables
	uv run scripts/cli.py db drop

db-reset: ## Reset database schema (drop and recreate all tables)
	uv run scripts/cli.py db reset

# Seeding commands
seed: ## Seed the database with sample data
	uv run scripts/cli.py seed

seed-fresh: ## Clear and seed the database with fresh data
	uv run scripts/cli.py seed --clear

seed-clear: ## Clear all seed data from the database
	uv run scripts/cli.py seed clear

seed-reset: ## Reset seed data (clear + seed)
	uv run scripts/cli.py seed reset

test: ## Run tests
	uv run pytest

test-cov: ## Run tests with coverage
	uv run pytest --cov=app

lint: ## Run linting
	uvx ruff check .

lint-fix: ## Run linting and fix issues
	uvx ruff check . --fix

run: ## Run the development server
	uv run fastapi dev app/main.py

run-prod: ## Run the production server
	uv run fastapi run app/main.py
