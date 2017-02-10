#!/bin/bash

readonly SCRIPT_DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
readonly INSTALL_DIR="/usr/local/bin"
readonly DOWNLOAD_DIR="/tmp"

readonly TERRAFORM_VERSION="0.8.6"
readonly TERRAFORM_DOWNLOAD_URL="https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip"
readonly PACKER_VERSION="0.12.2"
readonly PACKER_DOWNLOAD_URL="https://releases.hashicorp.com/packer/${PACKER_VERSION}/packer_${PACKER_VERSION}_linux_amd64.zip"
readonly PYTHON_REQUIREMNTS_FILE="$SCRIPT_DIR/python_requirements.txt"

source "$SCRIPT_DIR/utils.sh"

prerequisites() {
    local curl_cmd=`which curl`
    local unzip_cmd=`which unzip`
    local python_cmd=`which python`
    local pip_cmd=`which pip`
    local system=$(uname)

    if [ -z "$curl_cmd" ]; then
        error "curl does not appear to be installed. Please install and re-run this script."
        exit 1
    fi

    if [ -z "$unzip_cmd" ]; then
        error "unzip does not appear to be installed. Please install and re-run this script."
        exit 1
    fi

    if [ -z "$python_cmd" ]; then
        error "python does not appear to be installed. Please install and re-run this script."
        exit 1
    fi

    if [ -z "$pip_cmd" ]; then
        error "pip does not appear to be installed. Please install and re-run this script."
        exit 1
    fi

    if [ "$system" == "Linux" ]; then
        distro=$(lsb_release -i)
        if [[ $distro == *"Ubuntu"* ]] || [[ $distro == *"Debian"* ]] ;then
            warn "Your running Debian based linux. You might need to install 'sudo apt-get install build-essential python-dev"
        else
            warn "Your linux system was not tested"
        fi
    else
        warn "Tested only on Ubuntu 14.04"
    fi

    [[ ! -f "$PYTHON_REQUIREMNTS_FILE" ]] && error "requirements '$PYTHON_REQUIREMNTS_FILE' does not exist or permssion issue.\nPlease check and rerun."
    # we want to be root to install / uninstall
    if [ "$EUID" -ne 0 ]; then
        error "Please run as root"
        exit 1
    fi
}

install_binary() {
    inf "--> Downloading $1 binary"
    curl -o "$1" "$2"

    inf "--> Extracting executable"
    unzip "$1" -d "$INSTALL_DIR"

    rm "$1"
}

main() {
    # Be unforgiving about errors
    set -euo pipefail

    prerequisites

    inf "--> Installing core requirements"
    sudo apt-get install build-essential python-dev

    inf "--> Installing Terraform"
    install_binary "$DOWNLOAD_DIR/terraform.zip" $TERRAFORM_DOWNLOAD_URL

    inf "--> Installing Packer"
    install_binary "$DOWNLOAD_DIR/packer.zip" $PACKER_DOWNLOAD_URL

    inf "--> Installing Ansible"
    pip install --no-cache-dir  --upgrade --requirement "$PYTHON_REQUIREMNTS_FILE"
}

[[ "$0" == "$BASH_SOURCE" ]] && main
