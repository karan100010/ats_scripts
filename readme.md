# Table of Contents

- # [Setting up Airflow on CentOS](#setup-airflow-on-centos)
  - ## [Setup Docker](#setup-docker)
  - ## [Setup the project](#setup-the-project)

<a name="#setup-airflow-on-centos"> </a>

# Setting up Airflow on CentOS

<a name="#setup-docker"></a>

## Setup Docker

Note: Folllow the latest instructions [here](https://docs.docker.com/engine/install/centos/)

### 1. Uninstall old versions

This is important to remove the old versions of docker from the system and always make sure the latest version is used.

`sudo yum remove docker docker-client docker-client-latest docker-common docker-latest docker-latest-logrotate docker-logrotate docker-engine`

### 2. Install the `yum-utils` package and add the docker repo

A collection of tools and programs for managing yum repositories, installing debug packages, source packages, extended information from repositories and administrationFind more about them [here](https://man7.org/linux/man-pages/man1/yum-utils.1.html)

`sudo yum install -y yum-utils`
`sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo`

### 3. Install Docker Components

Install the Docker Engine, containerd, and Docker Compose.

`sudo yum install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin`

Note: If prompted to accept the GPG key, verify that the fingerprint matches `060A 61C5 1B55 8A7F 742B 77AA C52F EB6B 621E 9F35`

<a name="#setup-the-project"> </a>

## Setup the project

Note: For a more detailed guide follow [this](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html)

### 1. Clone the repo

The repo consists of various scripts for the project. We need the `docker-compose.yaml` script to setup the docker airflow containers

`git clone https://github.com/karan100010/ats_scripts.git`

### 2. Make a new Directory for `airflow`

This directory is the airflow project directory and will contain the files and folders like dags, logs, etc. The name can be anything.

`mkdir airflow`

### 3. Copy the `docker-compose.yaml` from `ats_scripts` to `airflow`

We are copying the `docker-compose.yaml` to the project directory to create the containers. This file will hold all the deatils about the airflow instance.

Note: Currently setup with the LocalExcecutor

`cp ats_scripts/docker-compose.yaml airflow/docker-compose.yaml`

### 4. Switch the directory to `airflow`

`cd airflow`

### 5. Create the directory for `./logs`, `./plugins`, `./dags`, `./config`

`mkdir -p ./logs ./plugins ./dags ./config`

### 6. Setup the right Airflow user

`echo -e "AIRFLOW_UID=$(id -u)" > .env`

### 7. Start the containers in detached mode

`docker compose up -d`
