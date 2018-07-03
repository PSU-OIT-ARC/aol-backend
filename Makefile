package = aol
distribution = psu.oit.arc.$(package)
egg_name = $(distribution)
egg_info = $(egg_name).egg-info

venv ?= venv
venv_python ?= python3
bin = $(venv)/bin


venv: $(venv)
$(venv):
	$(venv_python) -m venv $(venv)

egg-info: $(egg_info)
$(egg_info):
	$(bin)/python setup.py egg_info

install: $(venv) $(egg_info)
	$(venv)/bin/pip install -r requirements.txt
reinstall: clean-install install

init: install
	$(bin)/mc init --overwrite
reinit: clean-egg-info clean-pyc clean-venv init

test: install
	LOCAL_SETTINGS_FILE="local.base.cfg#test" $(bin)/python manage.py test -k
run:
	@$(bin)/python manage.py runserver

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
