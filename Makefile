CODE = app config tests
VENV = .venv
VENV_BIN = $(VENV)/Scripts
TEST = $(VENV_BIN)/poetry run pytest --verbosity=2 --showlocals --log-level=DEBUG --strict-markers $(arg) -k "$(k)"

.PHONY: install
install: ## Install dependencies
	$(VENV_BIN)/poetry install --no-interaction --no-ansi

.PHONY: venv
venv:
	python -m venv $(VENV)
	$(VENV_BIN)/python -m pip install --upgrade pip
	$(VENV_BIN)/python -m pip install poetry
	$(VENV_BIN)/poetry install

.PHONY: run
run: ## Run App
	$(VENV_BIN)/poetry run python -m app

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
	$(VENV_BIN)/poetry run autoflake --recursive --in-place --remove-all-unused-imports $(CODE)
	$(VENV_BIN)/poetry run isort $(CODE)
	$(VENV_BIN)/poetry run black --line-length 79 --target-version py39 --skip-string-normalization $(CODE)
	$(VENV_BIN)/poetry run unify --in-place --recursive $(CODE)

.PHONY: lint
lint: ## Lint code
	$(VENV_BIN)/poetry run flake8 --jobs 4 --statistics --show-source $(CODE)
	$(VENV_BIN)/poetry run pylint --rcfile=setup.cfg $(CODE)
	$(VENV_BIN)/poetry run mypy $(CODE)
	$(VENV_BIN)/poetry run black --line-length 79 --target-version py39 --skip-string-normalization --check $(CODE)
	$(VENV_BIN)/poetry run pytest --dead-fixtures --dup-fixtures
	$(VENV_BIN)/poetry run safety check --full-report

.PHONY: check
check: format lint test ## Format and lint code then run tests