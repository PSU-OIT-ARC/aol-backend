DEFAULT_GOAL := help
.PHONY = help

package = aol
distribution = psu.oit.arc.$(package)
egg_name = $(distribution)
egg_info = $(egg_name).egg-info

venv ?= venv
venv_python ?= python3
venv_autoinstall ?= pip wheel
bin = $(venv)/bin


help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

venv: $(venv)
$(venv):
	$(venv_python) -m venv $(venv)

egg-info: $(egg_info)
$(egg_info):
	$(bin)/python setup.py egg_info

install: $(venv) $(egg_info)
	$(venv)/bin/pip install -r requirements.txt

init: install
	$(bin)/mc init --overwrite
reinit: clean-egg-info clean-pyc clean-venv init

test: settings_module="aol.settings.test"
test: install
	@DJANGO_SETTINGS_MODULE=$(settings_module) $(bin)/python manage.py test --keepdb --failfast
test_container: install
	$(bin)/docker-compose run --user=aol --rm --entrypoint=/entrypoint-test.sh aol
shell: settings_module="aol.settings.development"
shell:
	@DJANGO_SETTINGS_MODULE=$(settings_module) $(bin)/python manage.py shell
run: settings_module="aol.settings.development"
run:
	@DJANGO_SETTINGS_MODULE=$(settings_module) $(bin)/python manage.py runserver
celery: settings_module="aol.settings.development"
celery:
	@DJANGO_SETTINGS_MODULE=$(settings_module) $(bin)/celery -A aol worker -l INFO

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

update_pip_requirements:  ## Updates python dependencies
	@if [ ! -d "./release-env" ]; then python3 -m venv ./release-env; fi
	@./release-env/bin/pip install --upgrade $(venv_autoinstall)
	@./release-env/bin/pip install --upgrade --upgrade-strategy=eager -r requirements.txt
	@./release-env/bin/pip freeze > requirements-frozen.txt
	@sed -i '1 i\--find-links https://packages.wdt.pdx.edu/dist/' requirements-frozen.txt
	@./release-env/bin/pip list --outdated

.PHONY = init reinit test run deploy \
         clean clean-all clean-build clean-dist clean-egg-info clean-pyc clean-venv
