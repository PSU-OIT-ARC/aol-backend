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

egg_version = $(shell git grep 'psu.oit.arc.aol' requirements-frozen.txt | cut -d"=" -f3)


help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

test:  ## Runs tests in current environment
	@$(bin)/python manage.py test --keepdb --failfast
test_container:  ## Runs tests in docker environment
	$(docker_compose) -f docker-compose.dev.yml run --user=aol --rm -e EMCEE_APP_CONFIG=app.test.yml -e APP_SERVICE=test app
shell:
	$(bin)/python manage.py shell
run:
	$(bin)/python manage.py runserver
celery:
	$(bin)/celery -A aol worker -l INFO

update_pip_requirements:  ## Updates python dependencies
	@echo "Updating Python requirements for v$(egg_version)..."; echo ""
	@if [ ! -d "./release-env" ]; then python3 -m venv ./release-env; fi
	@./release-env/bin/pip install --upgrade $(venv_autoinstall)
	@./release-env/bin/pip install --upgrade --upgrade-strategy=eager -r requirements.txt
	@./release-env/bin/pip freeze > requirements-frozen.txt
	@sed -i '1 i\--find-links https://packages.wdt.pdx.edu/dist/' requirements-frozen.txt
	@sed -i '/-e git+ssh:\/\/git@github.com\/PSU-OIT-ARC\/aol-backend.git/d' ./requirements-frozen.txt
	@sed -i '1 a\psu.oit.arc.aol==$(egg_version)' ./requirements-frozen.txt
	@./release-env/bin/pip install --upgrade --upgrade-strategy=eager -r requirements-dev.txt
	@./release-env/bin/pip freeze > docker/requirements-frozen.txt
	@sed -i '1 i\--find-links https://packages.wdt.pdx.edu/dist/' docker/requirements-frozen.txt
	@sed -i '/psu.oit.arc.aol/d' ./docker/requirements-frozen.txt
	@./release-env/bin/pip list --outdated
