#!/usr/bin/env just
set windows-shell := ["C:\\Program Files\\Git\\bin\\sh.exe", "-c"]

[private]
PYTHON_DIR := if os_family() == "windows" { "./.venv/Scripts" } else { "./.venv/bin" }
[private]
PYTHON := PYTHON_DIR + if os_family() == "windows" { "/python.exe" } else { "/python3" }
[private]
SYSTEM_PYTHON := if os_family() == "windows" { "py.exe" } else { "python3" }
[private]
IPYTHON := PYTHON_DIR + if os_family() == "windows" { "/ipython3.exe" } else { "/ipython3" }
[private]
RUFF := PYTHON_DIR + if os_family() == "windows" { "/ruff.exe" } else { "/ruff" }
[private]
MYPY := PYTHON_DIR + if os_family() == "windows" { "/mypy.exe" } else { "/mypy" }

_default:
	@just tasks

# List tasks
tasks:
	@just --list --unsorted

# Setup
setup:
    #!/usr/bin/env sh
    set -euo pipefail
    if test ! -e .venv; then
        {{ SYSTEM_PYTHON }} -m venv .venv;
        {{ PYTHON }} -m pip install --upgrade pip;
        {{ PYTHON }} -m pip install --upgrade --requirement requirements.txt;
    fi

# Upgrade requirements
upgrade-requirements:
    {{ PYTHON }} -m pip install --upgrade pip
    {{ PYTHON }} -m pip install --upgrade --requirement requirements.txt

# Setup development environment
setup-dev: setup
    #!/usr/bin/env sh
    set -euo pipefail
    if test ! -e {{ RUFF }}; then
        {{ PYTHON }} -m pip install --upgrade --requirement requirements-dev.txt
    fi

# Upgrade dev requirements
upgrade-dev-requirements: upgrade-requirements
    {{ PYTHON }} -m pip install --upgrade --requirement requirements-dev.txt

# Run `ipython`
ipython: setup-dev
    @({{ IPYTHON }} -i -c 'from rich import inspect; from rich.traceback import install as _tinstall; from rich.pretty import install as _pinstall; _tinstall(show_locals=True); _pinstall()')


# Run `ruff`
ruff *args: setup-dev
    @{{ RUFF }} {{ args }} .

# Organize imports and format code
format:
    @just ruff check . --select I --fix
    @just ruff format

# Run `mypy`
mypy *args: setup-dev
    @{{ MYPY }} {{ args }} .

# Format and lint code
lint: format
    @just ruff check
    @just mypy