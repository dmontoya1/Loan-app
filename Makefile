make build.PHONY: help build up down restart logs shell migrate createsuperuser collectstatic

help: ## Mostrar esta ayuda
	@echo "Comandos disponibles:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

build: ## Construir las imágenes de Docker
	docker-compose -f docker-compose.dev.yml build

up: ## Iniciar los contenedores
	docker-compose -f docker-compose.dev.yml up -d

down: ## Detener los contenedores
	docker-compose -f docker-compose.dev.yml down

restart: ## Reiniciar los contenedores
	docker-compose -f docker-compose.dev.yml restart

logs: ## Ver logs de los contenedores
	docker-compose -f docker-compose.dev.yml logs -f

shell: ## Abrir shell en el contenedor web
	docker-compose -f docker-compose.dev.yml exec web bash

migrate: ## Ejecutar migraciones
	docker-compose -f docker-compose.dev.yml exec web python manage.py migrate

makemigrations: ## Crear migraciones
	docker-compose -f docker-compose.dev.yml exec web python manage.py makemigrations

createsuperuser: ## Crear superusuario
	docker-compose -f docker-compose.dev.yml exec web python manage.py createsuperuser

collectstatic: ## Recolectar archivos estáticos
	docker-compose -f docker-compose.dev.yml exec web python manage.py collectstatic --noinput

test: ## Ejecutar tests
	docker-compose -f docker-compose.dev.yml exec web python manage.py test

clean: ## Limpiar contenedores, imágenes y volúmenes
	docker-compose -f docker-compose.dev.yml down -v
	docker system prune -f

setup: build up migrate createsuperuser ## Setup completo: construir, iniciar, migrar y crear superusuario
