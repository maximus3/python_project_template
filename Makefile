ifeq ($(shell test -e '.env' && echo -n yes),yes)
	include .env
endif

VENV = .venv
ifeq ($(OS),Windows_NT)
	PYTHON_EXECUTABLE = python
	VENV_BIN = $(VENV)/Scripts
else
    PYTHON_EXECUTABLE = python3
    VENV_BIN = $(VENV)/bin
endif

POETRY_VERSION=1.1.13
POETRY_RUN = poetry run

# Manually define main variables

APPLICATION_NAME = app

ifndef APP_PORT
override APP_PORT = 8000
endif

ifndef APP_HOST
override APP_HOST = 127.0.0.1
endif

args := $(wordlist 2, 100, $(MAKECMDGOALS))
ifndef args
MESSAGE = "No such command (or you pass two or many targets to ). List of possible commands: make help"
else
MESSAGE = "Done"
endif

TEST = $(POETRY_RUN) pytest --verbosity=2 --showlocals --log-level=DEBUG
CODE = $(APPLICATION_NAME) tests

HELP_FUN = \
	%help; while(<>){push@{$$help{$$2//'options'}},[$$1,$$3] \
	if/^([\w-_]+)\s*:.*\#\#(?:@(\w+))?\s(.*)$$/}; \
    print"$$_:\n", map"  $$_->[0]".(" "x(20-length($$_->[0])))."$$_->[1]\n",\
    @{$$help{$$_}},"\n" for keys %help; \

# Commands

.PHONY: help
help: ##@Help Show this help
	@echo -e "Usage: make [target] ...\n"
	@perl -e '$(HELP_FUN)' $(MAKEFILE_LIST)


.PHONY: env
env:  ##@Environment Create .env file with variables
	@$(eval SHELL:=/bin/bash)
	@cp .env.example .env
	@echo "SECRET_KEY=$$(openssl rand -hex 32)" >> .env


.PHONY: venv
venv: ##@Environment Create virtual environment, no need in docker
	$(PYTHON_EXECUTABLE) -m venv $(VENV)
	$(VENV_BIN)/python -m pip install --upgrade pip
	$(VENV_BIN)/python -m pip install poetry==$(POETRY_VERSION)
	$(VENV_BIN)/poetry config virtualenvs.create true
	$(VENV_BIN)/poetry config virtualenvs.in-project true
	$(VENV_BIN)/poetry install --no-interaction --no-ansi

.PHONY: install
install: ##@Code Install dependencies
	poetry install --no-interaction --no-ansi

.PHONY: up
up: ##@Application Up App
	$(POETRY_RUN) python -m app

.PHONY: migrate
migrate:  ##@Database Do all migrations in database
	alembic upgrade $(args)

.PHONY: revision
revision:  ##@Database Create new revision file automatically with prefix (ex. 2022_01_01_14cs34f_message.py)
	alembic revision --autogenerate

.PHONY: db
db: ##@Database Docker up db
	docker-compose up -d postgres

.PHONY: test
test: ##@Testing Runs pytest with coverage
	make db && $(TEST) --cov

.PHONY: test-fast
test-fast: ##@Testing Runs pytest with exitfirst
	make db && $(TEST) --exitfirst

.PHONY: test-failed
test-failed: ##@Testing Runs pytest from last-failed
	make db && $(TEST) --last-failed

.PHONY: test-cov
test-cov: ##@Testing Runs pytest with coverage report
	make db && $(TEST) --cov --cov-report html

.PHONY: format
format: ###@Code Formats all files
	$(POETRY_RUN) autoflake --recursive --in-place --remove-all-unused-imports $(CODE)
	$(POETRY_RUN) isort $(CODE)
	$(POETRY_RUN) black --line-length 79 --target-version py39 --skip-string-normalization $(CODE)
	$(POETRY_RUN) unify --in-place --recursive $(CODE)

.PHONY: lint
lint: ###@Code Lint code
	$(POETRY_RUN) flake8 --jobs 4 --statistics --show-source $(CODE)
	$(POETRY_RUN) pylint --rcfile=setup.cfg $(CODE)
	$(POETRY_RUN) mypy $(CODE)
	$(POETRY_RUN) black --line-length 79 --target-version py39 --skip-string-normalization --check $(CODE)
	$(POETRY_RUN) pytest --dead-fixtures --dup-fixtures
	$(POETRY_RUN) safety check --full-report || echo "Safety check failed"

.PHONY: check
check: format lint test ###@Code Format and lint code then run tests

.PHONY: docker-up
docker-up: ##@Application Docker up
	docker-compose up

.PHONY: docker-up-d
docker-up-d: ##@Application Docker up detach
	docker-compose up -d

.PHONY: docker-build
docker-build: ##@Application Docker build
	docker-compose build

.PHONY: docker-down
docker-down: ##@Application Docker down
	docker-compose down

.PHONY: docker-clean
docker-clean: ##@Application Docker prune -f
	docker image prune -f

.PHONY: docker
docker: docker-clean docker-build docker-up-d docker-clean ##@Application Docker prune, up, run and prune

%::
	echo $(MESSAGE)

