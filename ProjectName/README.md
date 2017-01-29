# <% project_title %>

- run `make setup` to install system requirements (if you don't want to do it please see [local development](#local-development) section)
- setup and activate virtual environment by running `virtualenv -p python3.6 .venv && source .venv/bin/activate`
- run `make develop` to install project as a program inside virtual environment
- run `<% project_name %> django runserver` to run django development server
- navigate in your browser to `http://localhost:8000` and browse your site (use <% project_name|lower %> as username and test as password)

To run uwsgi server run `<% project_name %> web run` and go to `http://localhost` in your browser to browse the site.

## Local development

If you have more complex infrastructure during development you want to run it in separate environment. For this you can
use 2 options:

- run `make provision local:docker` to create Docker images using Ansible and Packer to run development environment
- run `make provision local:vagrant` to create Vagrant vms using Ansible and Packer. Because Vagrant is using more.

Since creating multiple Vagrant machines will use a lot of resources you can also create Vagrant machine and deploy
Docker containers there.

To do this run `make provision local:vagrantdocker`.

## Provisioning

To create resources for your development, staging and production environment we are using Terraform which uses images
build with Packer. AWS is default resource provider. Please edit `devops/ansible/vpass` file to provide Ansible-Valut
password for secerets encryption and `devops/ansible/terraform/secrets` to provide AWS secrets (both of those files are
excluded from git repo).

Because AWS resources are expensive in comparison to other providers we suggest better option would be to change them
for it's cheaper substitutes.

### Development environment

Run `make provision development` to provision development environment.

### Staging environment

Run `make provision staging` to provision development environment.

### Staging environment

Run `make provision production` to provision development environment.

### Utils environment

Additionally there is posibility to use default GOCD CI pipeline. You can deploy this environment locally, similary to
setting up local environment by running two options:

- run `make provision local:docker` to create utils environment in Docker container
- run `make provision local:vagrant` to create utils environment using Vagrant VM

To provision utils environment into remote resources please use following command: `make provision utils`
