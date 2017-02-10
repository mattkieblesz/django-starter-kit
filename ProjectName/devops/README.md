## Installation

First install requirements by calling `sudo make setup`. Then update vendor roles with `make updateroles`. To be able to use
provisioning tools you need to export access keys to resource providers and basic configuration files setup. Run `source setup.cfg`
and `source secrets.cfg` to export them to current environment..

## Layout

    .gitignore (exclude all secrets/images/resource state)
    ansible.cfg                 # global ansible config
    secrets                     # secret variables excluded from git
    variables                   # basic configuration variables
    secrets-template            # secrets template
    vpass                       # ansible vault password file

    files/                      # Files to share for all envs
      ssh_keys/                 # list of ssh keys
        id_username.pub

    group_vars/                 # for default role setup
      all/                      # variables under this directory belongs all the groups
        role1.yml               # role1 variable file for all groups
        role2.yml               # role2 variable file for all groups
      play1/                    # here we assign variables to play1 groups
        role1.yml               # Each file will correspond to a role i.e. role1.yml
        role2.yml               # --||--
      play2/                    # here we assign variables to play2 groups
        role3.yml               # Each file will correspond to a role i.e. role3.yml
        role4.yml               # --||--
      testplay/                 # here we assign variables to testplay groups
        role5.yml               # Each file will correspond to a role i.e. role5.yml
        role6.yml               # --||--
      performancetestplay/      # here we assign variables to performancetestplay groups
        role7.yml               # Each file will correspond to a role i.e. role7.yml
        role8.yml               # --||--
      jenkinsplay/              # here we assign variables to jenkinsplay groups
        role9.yml               # Each file will correspond to a role i.e. role9.yml
        role10.yml              # --||--
      gocdplay/                 # here we assign variables to gocdplay groups
        role11.yml              # Each file will correspond to a role i.e. role11.yml
        role12.yml              # --||--

    plays/
      play1.yml                 # playbooks should have just services roles dependencies
      play2.yml                 # --||--
      performancetestplay.yml   # --||--
      jenkinsplay.yml           # --||--
      gocdplay.yml              # --||--
      testplay.yml              # --||--

    roles/
      services/                 # All the roles that are specific to a service
        role1/
          rolestuff
        role2/
          rolestuff
        role3/
          rolestuff
        role4/
          rolestuff
        role5/
          rolestuff
        role6/
          rolestuff
        role7/
          rolestuff
        role8/
          rolestuff
        role9/
          rolestuff
        role10/
          rolestuff
      js_roles/                 # All the roles that common to different roles
        commonrole1/
          rolestuff
      vendor/                   # All the roles that are in git or ansible galaxy (excluded from git)
        role11/
          rolestuff
        role12/
          rolestuff
      requirements.yml          # All the information about external roles

    envs/                       # Main entry point to infrastructure setup
      dev/
        vars/                   # Folder with vars specific to environment (simple flat file structure)
          all.yml
          play1.yml
          play2.yml
          secret-plain.yml      # Secret file template (not used)
          secrets.yml           # One file with secrets for environment
        inventory.ini           # Dynamic inventory file which includes location
        terraform.tf            # Environment infra as code setup
      stg
        ...
        terraform.tf            # Linked from prd environment (will be used with different vars)
      prd
        ...
      mgt
        ...
      tst
        ...
      prf
        ...

    scripts/                    # utility scripts used by Makefile targets
      setup.sh                  # setup devops script
      update_roles.sh           # update vendor roles
      create_role.sh            # create new common/service role
      create_env.sh             # create new environment

    templates/                  # templates used in this repo
      Vagrant.j2                # vagrant template used for this environment

    Makefile                    # Management interface which can be used by any dev from the start
      setup                     # setup devops toolset on current machine
      updateroles               # update ansible vendor roles
      createrole                # creates new role
      createsecret              # creates new secret file
      <action> loction=<local/remote/docker/vagrant>, build=<version/commit>, env=<tst/mgt/dev/stg/prd/prf/...>, play=<play1/play2/...>
        test                    # mgt tool to run test suite
        build                   # mgt tool to build images
        create                  # mgt tool to create infrastructure as code
        destroy                 # mgt tool to destroy infrastructure as code
        provision               # mgt tool to provision to already created infrastructure
        provision-tag           # mgt tool to provision specific task to already created infrastructure like collectstatic in remote, deploy code, migrate ...
      custom                    # custom utility used only on local


## Resource naming convention

In order to simplify life we assume one resource provider account will be used. Therefore there needs to be naming
which will include:
- environment
- location
- role
- resource number

Examples: `prd-lo-web-1`, `dev-ir-db-1`, `prf-fr-db-1`, `stg-lo-celery-3`, `mgt-lo-ci-1`
