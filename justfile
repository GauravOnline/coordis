set windows-shell := ["C:\\Program Files\\Git\\bin\\sh.exe", "-c"]

_tasks: tasks

# List tasks
tasks:
	@just --list --unsorted

_setup_poetry:
	@(POETRY_VIRTUALENVS_IN_PROJECT=true poetry install)

# SetUp project
setup: _setup_poetry
	@poetry run pre-commit install

# Run 'ruff'
ruff *args:
	@poetry run ruff {{ args }} .

# 'ruff --fix'
ruff-fix:
	@just ruff check . --fix

# Run organize imports and format all code
format:
	@just ruff check . --select I --fix
	@just ruff format

# Run mypy
mypy *args:
	@poetry run mypy {{ args }} .

# Lint code
lint: format
	@just ruff check
	@just mypy

# Build project
build: _setup_poetry
	@poetry build

# Install program using pipx
install: build
	@py -m pipx install ./dist/`ls -t dist | head -n2 | grep whl`

# Uninstall program using pipx
uninstall:
	@py -m pipx uninstall coordis

# Reinstall program using pipx
reinstall: uninstall
	@just install
