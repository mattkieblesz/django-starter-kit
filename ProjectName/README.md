# <% project_name %>

- run `make setup` to install system requirements
- setup and activate virtual environment by running `virtualenv -p python3.6 .venv && source .venv/bin/activate`
- run `make develop` to install project as a program inside virtual environment
- run `<% project_name %> django runserver` to run django development server
- navigate in your browser to `http://localhost:8000` and browse your site

To run uwsgi server run `<% project_name %> web run` and go to `http://localhost` in your browser to browse the site.
