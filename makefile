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
	$(DOCKER_COMPOSE) down

build_up: ## Собирает и запускает сервисы сразу
	$(DOCKER_COMPOSE) up --build -d

restart: ## Перезапускает сервисы
	$(DOCKER_COMPOSE) down && $(DOCKER_COMPOSE) up -d

logs: ## Показывает логи контейнеров
	$(DOCKER_COMPOSE) logs -f

# Установка зависимостей через Poetry
install: ## Устанавливает зависимости через Poetry
	$(DOCKER_COMPOSE) run web-app $(POETRY) install

# Django-команды
migrate: ## Выполняет миграции базы данных
	$(DOCKER_COMPOSE) exec web-app $(POETRY) run python manage.py migrate

shell: ## Запускает интерактивную оболочку Django
	$(DOCKER_COMPOSE) exec web-app $(POETRY) run python manage.py shell

# Celery-команды
worker: ## Запускает Celery worker
	$(DOCKER_COMPOSE) up -d worker

cleaner: ## Запускает Celery beat
	$(DOCKER_COMPOSE) up -d worker-cleaner

# Nginx
nginx: ## Запускает Nginx-сервис
	$(DOCKER_COMPOSE) up -d nginx

# Тестирование
test: ## Запускает тесты через Poetry
	$(DOCKER_COMPOSE) exec web-app $(POETRY) run pytest

