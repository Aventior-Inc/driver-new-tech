#!/bin/bash

set -e
# keep track of the last executed command
trap 'last_command=$current_command; current_command=$BASH_COMMAND' DEBUG
# echo an error message before exiting
trap 'echo "\"${last_command}\" command failed with exit code $?."' EXIT

export $(cat setup.conf)
echo $ECR_REPO
if ! command -v docker &> /dev/null; then
    echo "Docker not found, installing..."
    sudo apt-get update -y
    sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    echo "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    sudo apt-get update -y
    sudo DEBIAN_FRONTEND=noninteractive apt-get install -y docker-ce docker-ce-cli containerd.io
    sudo curl -L https://github.com/docker/compose/releases/download/v2.17.2/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
fi


# Ensure docker group exists and add the current user to it
if ! getent group docker > /dev/null; then
    echo "Docker group does not exist. Creating docker group..."
    sudo groupadd docker
fi

# Add the current user to the docker group
sudo usermod -aG docker $USER
echo "User $USER added to docker group. You may need to log out and log back in for the changes to take effect."

# Ensure AWS CLI is installed
echo "installing aws cli"
if ! command -v aws &> /dev/null; then
    echo "AWS CLI not found, installing..."
    sudo apt-get update -y
    sudo apt-get install -y unzip curl
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
    unzip awscliv2.zip
    sudo ./aws/install
fi

sudo mkdir -p /var/www/driver-new-tech
