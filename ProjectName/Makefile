NPM_ROOT = ./node_modules
STATIC_DIR = src/<% project_name %>/static

################
# System setup #
################

setup-system:
	@echo "--> Update apt repos"
	sudo add-apt-repository ppa:ubuntu-toolchain-r/test
	sudo add-apt-repository ppa:jonathonf/python-3.6
	sudo apt-get update
	@echo "--> Updating C compilers to 4.9 (for uwsgi to compile)"
	sudo apt-get install build-essential gcc-4.9 cpp-4.9 g++-4.9
	sudo rm /usr/bin/gcc /usr/bin/cpp /usr/bin/x86_64-linux-gnu-gcc
	sudo ln -s /usr/bin/gcc-4.9 /usr/bin/x86_64-linux-gnu-gcc
	sudo ln -s /usr/bin/gcc-4.9 /usr/bin/gcc
	sudo ln -s /usr/bin/cpp-4.9 /usr/bin/cpp
	@echo "--> Installing Python 3.6"
	sudo apt-get install python3.6 python3.6-dev
	sudo pip3 install virtualenv

setup-db:
	sudo apt-get install postgresql
	psql postgres -c "CREATE USER <% project_name %> WITH PASSWORD '<% project_name %>';"

setup: setup-system setup-db

#############
# Dev setup #
#############

setup-git:
	@echo "--> Setting up git repository"
	git init
	@echo "--> Installing git hooks"
	git config branch.autosetuprebase always
	cd .git/hooks && ln -sf ../../config/hooks/* ./
	@echo ""

install-python:
	@echo "--> Installing Python dependencies"
	pip install "setuptools>=31.0.0"
	# order matters here, base package must install first
	pip install -e .
	pip install "file://`pwd`#egg=<% project_name %>[dev]"

install-python-tests:
	pip install "file://`pwd`#egg=<% project_name %>[dev,tests]"

install-npm:
	@echo "--> Installing Node dependencies"
	npm install

develop: setup-git install-python install-python-tests install-npm build-semantic reset-db

###########
# Testing #
###########

test: develop lint test-python

testloop: develop
	pip install pytest-xdist
	py.test tests -f

test-python:
	@echo "--> Running Python tests"
	py.test tests/integration tests/<% project_name %> || exit 1
	@echo ""

test-acceptance:
	@echo "--> Building static assets"
	@${NPM_ROOT}/.bin/webpack -p
	@echo "--> Running acceptance tests"
	py.test tests/acceptance
	@echo ""

test-python-coverage:
	@echo "--> Running Python tests"
	coverage run --source=src/<% project_name %> -m py.test tests/integration tests/<% project_name %>
	@echo ""

lint: lint-python

lint-python:
	@echo "--> Linting python"
	flake8
	@echo ""

coverage:
	make test-python-coverage
	coverage html

##########
# Commit #
##########

build: locale build-assets

locale:
	cd src/<% project_name %> && <% project_name %> django makemessages -i static -l en
	cd src/<% project_name %> && <% project_name %> django compilemessages

# FIXME: for some reason semantic doesn't use source.site path properly so currently we build it in site directory
build-semantic:
	cd src/<% project_name %>/static/semantic && gulp build

build-assets: build-semantic
	<% project_name %> django collectstatic --no-input

watch-assets:
	cd src/<% project_name %>/static/semantic && gulp watch

#########
# Utils #
#########

clean:
	@echo "--> Cleaning __pycache__ folders"
	find . -type d -name "__pycache__" -exec rm -r "{}" \;
	@echo "--> Cleaning python build artifacts"
	rm -rf build/ dist/
	@echo "--> Cleaning built static files"
	cd src/<% project_name %>/static/semantic && gulp clean
	rm -rf static/
	@echo ""

############
# Database #
############

reset-db:
	@echo "--> Dropping existing '<% project_name %>' database"
	dropdb <% project_name %> || true
	@echo "--> Creating '<% project_name %>' database"
	createdb -E utf-8 <% project_name %>
	@echo "--> Applying migrations"
	<% project_name %> upgrade
