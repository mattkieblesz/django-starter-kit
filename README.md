# Django Starter Kit

- clone repo `git clone git@github.com:mattkieblesz/django-starter-kit.git`
- run `cd django-starter-kit`
- edit `config.json` to configure your starter kit
- run `make startproject`
- run `cd ../<projectname>` where projectname is the name of the project you put in `config.json` file
- checkout `Makefile` to see what's going to happen when you run following commands
- run `make setup` to install system requirements
- setup virtual environment by running `virtualenv -p python3.6 .venv && source .venv/bin/activate`
- run `make develop` to install project as a program inside virtual environment
- now you can import your project into your git remote
- run `<projectname> django runserver` to run django development server
- navigate in your browser to `http://localhost:8000` and browse your site
