# Environment (local, test, dev, staging, prod)
ENVIRONMENT ?= local
export ENVIRONMENT

PROJECT_NAME= api
API_IMAGE_NAME=${PROJECT_NAME}-api:${ENVIRONMENT}
DOCKERCOMPOSE_PATH=./docker/${ENVIRONMENT}.docker-compose.yml

# Build the Docker images
build:
	docker-compose -f ${DOCKERCOMPOSE_PATH} build --build-arg ENVIRONMENT=${ENVIRONMENT}

# Start services defined in docker-compose.yml, or specific service if service is set
up:
	@if [ -z "$(service)" ]; then \
		docker-compose -f ${DOCKERCOMPOSE_PATH} up -d; \
	else \
		docker-compose -f ${DOCKERCOMPOSE_PATH} up -d $(service); \
	fi

# Stop services defined in docker-compose.yml, or specific service if service is set
down:
	@if [ -z "$(service)" ]; then \
		docker-compose -f ${DOCKERCOMPOSE_PATH} down; \
	else \
		docker-compose -f ${DOCKERCOMPOSE_PATH} stop $(service); \
	fi

# Stop services, remove images, containers, volumes, and networks
clean:
	docker-compose -f ${DOCKERCOMPOSE_PATH} down -v --rmi all --remove-orphans
	docker image prune -f

# Delete the API Docker image
delete-images:
	docker rmi ${API_IMAGE_NAME}

# Lint the codebase
lint:
	isort --profile black ./src/
	black ./src/

# Run tests
test:
	@make up service=api
	@if [ -z "$(name)" ]; then \
		docker-compose -f ${DOCKERCOMPOSE_PATH} exec api pytest -p no:warnings; \
	else \
		docker-compose -f ${DOCKERCOMPOSE_PATH} exec api pytest -p no:warnings -k $(name); \
	fi

# Create new migrations based on model changes
migrations:
	@make up service=postgres
	POSTGRES_HOST="localhost" python src/manage.py makemigrations

# Apply migrations
migrate:
	@make up service=api
	docker-compose -f ${DOCKERCOMPOSE_PATH} exec api python manage.py migrate

# Creates a super-user
create-super-user:
	@make up service=api
	docker-compose -f ${DOCKERCOMPOSE_PATH} exec api python manage.py createsuperuser

# Compiles the requirements
compile-req:
	pip-compile requirements/${ENVIRONMENT}.requirements.in -o requirements/${ENVIRONMENT}.requirements.txt

# Create PO translation files
translations:
	python src/manage.py makemessages --all --ignore=env

# Validate translation files
validate-translations:
	@for file in src/greengo/locale/*/*/*.po; do \
		msgfmt --check -o /dev/null $$file || echo "Error in $$file"; \
	done

# Compile translation files
compile-translations:
	python src/manage.py compilemessages 

# Print variables (useful for debugging the Makefile)
print-%  : ; @echo $* = $($*)

.PHONY: build up down clean test delete-images migrations migrate create-super-user compile-req translations compile-translations
