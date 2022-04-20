CODE = app config tests

VENV = .venv
ifeq ($(OS),Windows_NT)
	PYTHON_EXECUTABLE = python
	VENV_BIN = $(VENV)/Scripts
else
    PYTHON_EXECUTABLE = python3
    VENV_BIN = $(VENV)/bin
endif

TEST = $(VENV_BIN)/poetry run pytest --verbosity=2 --showlocals --log-level=DEBUG --strict-markers $(arg) -k "$(k)"

POETRY_VERSION=1.1.5
POETRY_RUN = poetry run

DOCKER_NAME = test-app
DOCKER_IMAGE = $(DOCKER_NAME)


.PHONY: help
help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: venv
venv: ## Create virtual environment, no need in docker
	$(PYTHON_EXECUTABLE) -m venv $(VENV)
	$(VENV_BIN)/python -m pip install --upgrade pip
	$(VENV_BIN)/python -m pip install poetry==$(POETRY_VERSION)
	$(VENV_BIN)/poetry install --no-interaction --no-ansi

.PHONY: install
install: ## Install dependencies
	poetry install --no-interaction --no-ansi

.PHONY: run
run: ## Run App
	$(POETRY_RUN) python -m app

.PHONY: test
test: ## Runs pytest with coverage
	$(TEST) --cov=app

.PHONY: test-fast
test-fast: ## Runs pytest with exitfirst
	$(TEST) --exitfirst

.PHONY: test-failed
test-failed: ## Runs pytest from last-failed
	$(TEST) --last-failed

.PHONY: test-cov
test-cov: ## Runs pytest with coverage report
	$(TEST) --cov --cov-report html

.PHONY: format
format: ## Formats all files
	$(POETRY_RUN) autoflake --recursive --in-place --remove-all-unused-imports $(CODE)
	$(POETRY_RUN) isort $(CODE)
	$(POETRY_RUN) black --line-length 79 --target-version py39 --skip-string-normalization $(CODE)
	$(POETRY_RUN) unify --in-place --recursive $(CODE)

.PHONY: lint
lint: ## Lint code
	$(POETRY_RUN) flake8 --jobs 4 --statistics --show-source $(CODE)
	$(POETRY_RUN) pylint --rcfile=setup.cfg $(CODE)
	$(POETRY_RUN) mypy $(CODE)
	$(POETRY_RUN) black --line-length 79 --target-version py39 --skip-string-normalization --check $(CODE)
	$(POETRY_RUN) pytest --dead-fixtures --dup-fixtures
	$(POETRY_RUN) safety check --full-report

.PHONY: check
check: format lint test ## Format and lint code then run tests

.PHONY: docker-build
docker-build: ## Build docker image
	docker build -t $(DOCKER_IMAGE) .

.PHONY: docker-rm
docker-rm: ## Remove docker image
	docker image rm $(DOCKER_IMAGE)

.PHONY: docker-rm-none
docker-rm-none: ## Remove all untagged docker images
	docker images | grep "<none>" | awk '{print $3}' | xargs docker rmi

.PHONY: docker-run
docker-run: ## Run docker image
	docker container run -d --rm --name $(DOCKER_NAME) $(DOCKER_IMAGE)

.PHONY: docker-run-it
docker-run-it: ## Run docker image interactive
	docker run -it $(DOCKER_IMAGE)

.PHONY: docker-all
docker-all: docker-rm docker-build docker-run ## Docker rm, build and run