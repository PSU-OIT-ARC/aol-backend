venv ?= .env
venv_python ?= python3
bin = $(venv)/bin


local.dev.cfg:
	echo '[dev]' >> $@
	echo 'extends = "local.base.cfg"' >> $@

local.test.cfg:
	echo '[test]' >> $@
	echo 'extends = "local.base.cfg"' >> $@

venv: $(venv)
$(venv):
	$(venv_python) -m venv $(venv)

install: $(venv)
	$(venv)/bin/pip install -r requirements.txt

init: install local.dev.cfg local.test.cfg
	$(bin)/runcommand init --overwrite
	$(bin)/runcommand test
reinit: clean-egg-info clean-pyc clean-venv init

test:
	$(bin)/runcommand test

run:
	$(bin)/runcommand runserver

clean: clean-pyc
clean-all: clean-build clean-dist clean-egg-info clean-pyc clean-venv
clean-build:
	rm -rf build
clean-dist:
	rm -rf dist
clean-egg-info:
	rm -rf *.egg-info
clean-pyc:
	find . -name __pycache__ -type d -print0 | xargs -0 rm -r
	find . -name '*.py[co]' -type f -print0 | xargs -0 rm
clean-venv:
	rm -rf $(venv)

.PHONY = init reinit test run deploy \
         clean clean-all clean-build clean-dist clean-egg-info clean-pyc clean-venv
