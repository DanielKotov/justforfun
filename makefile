# Переменные
DOCKER_COMPOSE = docker compose
POETRY = poetry

# Служебные цели
.PHONY: help build up down logs restart install migrate worker cleaner nginx shell test

help:  ## Показывает список доступных команд
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

# Команды Docker Compose
build: ## Собирает Docker-контейнеры
	$(DOCKER_COMPOSE) build

up: ## Поднимает сервисы в фоне
	$(DOCKER_COMPOSE) up -d

down: ## Останавливает все сервисы
	$(DOCKER_COMPOSE) down -v

build_up: ## Собирает и запускает сервисы сразу
	$(DOCKER_COMPOSE) up --build -d

restart: ## Перезапускает сервисы
	$(DOCKER_COMPOSE) down && $(DOCKER_COMPOSE) up -d

logs: ## Показывает логи контейнеров
	$(DOCKER_COMPOSE) logs -f

# Тестирование
test: ## Запускает тесты через Poetry
	$(DOCKER_COMPOSE) exec web-app $(POETRY) run pytest

