.PHONY:help

PROJECT_NAME_DEV = oneflask_dev
PROJECT_NAME_PROD = oneflask_prod
DOCKER_COMMAND_DEV = docker-compose -p $(PROJECT_NAME_DEV) -f docker/docker-compose.dev.yml

help: ## Help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

up: ## Start development containers
	@echo "Starting development containers"
	@$(DOCKER_COMMAND_DEV) up -d --build

down: ## Remove development containers
	@echo "Removing development containers"
	@$(DOCKER_COMMAND_DEV) down

clean: ## Remove development containers and volumes
	@echo "Removing development containers and volumes"
	@$(DOCKER_COMMAND_DEV) down -v