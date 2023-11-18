# Table of Contents

- # [Setting up Airflow on CentOS](#setup-airflow-on-centos)

  - ## [Setup Docker](#setup-docker)
  - ## [Setup the Airflow](#setup-the-project)

- # [Setup ChromaDB on CentOS](#setup-chromadb)
- # [Setup Speechbrain on CentOS](#speechbrain)

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

### 7. Start the docker engine

Start the docker engine if not already running

`sudo systemctl start docker`

### 8. Start the containers in detached mode

`docker compose up -d`

<a name="#setup-chromadb"></a>

# Setup ChromaDB

### 1. Clone the repo

Clone the official chromaDB repo as we will need it to build a docker image ofchormaDB from source.

`git clone https://github.com/chroma-core/chroma.git`

### 2. Switch into the repo

Change the directory and verify that `docker-compose.yml` and `Dockerfile` in the repo. We can modify these if needed to change the default behaivior of the container.

`cd chroma`
`ls`

### 3. Start the docker engine

Start the docker engine if not already running

`sudo systemctl start docker`

### 4. Run docker compose

`sudo docker compose up -d`

### 5. Verify everything

Verify that the container has started. There should be a `chroma-server-1` container running.

`sudo docker ps`

Also verify the database is operational by sending a curl request

`curl http://localhost:8000/api/v1/heartbeat`

This should return a nanosecond heartbeat like below

`{"nanosecond heartbeat":1700043941276595546}`

<a name="#speechbrain"> </a>

# Setup Speechbrain on CentOS

Speechbrain is the language identification model used to detect the language being spoken in the audiofile. We will be deploying speechbrain wrapped in a flask api with a single endpoint which is used to interact with the model.

### 1. Clone the repo

Clone the repo for ats_scripts. (skip if done already)

`git clone https://github.com/karan100010/ats_scripts.git`

### 2. Switch the directory

Switch to the speechbrain dicretory inside ats_scripts

`cd ./ats_scripts/speechbrain`

### 3. Build the docker image for speechbrain

Create a docker image for speechbrain that is used to run the container.

`docker build -t speechbrain-li .`

### 4. Create and Start the container for speechbrain

Now create the container `speechbrain-li` which will have a flask server on the container on the port 5000. This can be used to send a post request on the `/predict_language` endpoint to get the results.

`docker run -p 5000:5000 --name speechbrain-li-container speechbrain-li`

### 5. Verify the container is running

Verify the container named `speechbrain-li` is running by running the following command

`docker ps`

You can also verify the api by seding a dummy post request to the model using curl

`curl -X POST -H "Content-Type: application/json" -d "{\"filepath\":\"https://omniglot.com/soundfiles/udhr/udhr_th.mp3\"}" http://localhost:5000/predict_language`
