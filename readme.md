# Table of Contents

- ## [Setup Docker](#setup-docker-1)
- ## [Setup The Project](#setup-the-project-1)
- ## [Setup Airflow on CentOS](#setup-airflow-on-centos-1)
- ## [Setup ChromaDB on CentOS](#setup-chromadb-on-centos-1)
- ## [Setup Nemo English on CentOS](#setup-nemo-english-on-centos-1)
- ## [Setup Nemo Hindi on CentOS](#setup-nemo-hindi-on-centos-1)
- ## [Setup Spacy on CentOS](#setup-spacy-on-centos-1)
- ## [Setup Speechbrain on CentOS](#setup-speechbrain-on-centos-1)

# Setup Docker

Note: Folllow the latest instructions [here](https://docs.docker.com/engine/install/centos/)

## 1. Uninstall old versions

This is important to remove the old versions of docker from the system and always make sure the latest version is used.

`sudo yum remove docker docker-client docker-client-latest docker-common docker-latest docker-latest-logrotate docker-logrotate docker-engine`

## 2. Install the `yum-utils` package and add the docker repo

A collection of tools and programs for managing yum repositories, installing debug packages, source packages, extended information from repositories and administrationFind more about them [here](https://man7.org/linux/man-pages/man1/yum-utils.1.html)

`sudo yum install -y yum-utils`
`sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo`

## 3. Install Docker Components

Install the Docker Engine, containerd, and Docker Compose.

`sudo yum install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin`

Note: If prompted to accept the GPG key, verify that the fingerprint matches `060A 61C5 1B55 8A7F 742B 77AA C52F EB6B 621E 9F35`

# Setup The Project

## 1. Clone the repo

The repo consists of various scripts for the project. We need the `docker-compose.yaml` script to setup the docker airflow containers

`git clone https://github.com/karan100010/ats_scripts.git`

## 2. Switch the directory

Change the directory to `ats-scripts`

`cd ats-scripts`

# Setup Airflow on CentOS

Apache Airflow is an open-source platform simplifying data workflow automation, leveraging Python for code-centric flexibility, dynamic extensibility, and reliable scalability.

## 1. Switch the directory

Change the directory to `airflow` in the `ats_scripts` directory

`cd airflow`

## 2. Setup the right Airflow user

`echo -e "AIRFLOW_UID=$(id -u)" > .env`

## 3. Start the docker engine

Start the docker engine if not already running

`sudo systemctl start docker`

## 4. Run docker compose

The directory consists of `docker-compose.yaml` which file will hold all the deatils about the airflow instance. Use the below command to run the airflow containers.

`docker-compose up -d`

Note: Currently airflow is setup with the LocalExcecutor. To change this make necessary adjustments to the `docker-compose.yaml` file. For a more detailed guide follow [this](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html)

## 5. Check the containers are running

Make sure the containers are running. You will get a list of all the running containers.

`docker ps`

Login to the airflow web dashboard by going to `http://localhost:8080`. The default username and password is `airflow`.

Note: The default `username` and `password` can be changed by modifying the `docker-compose.yaml`.

# Setup ChromaDB on CentOS

Chroma is an open-source vector database. A vector database is a type of database system optimized for the storage, retrieval, and efficient querying of vector data, commonly used in applications such as machine learning and similarity search.

## 1. Switch the directory

Change the directory to `chroma` in the `ats_scripts` directory

`cd chroma`

## 2. Start the docker engine

Start the docker engine if not already running

`sudo systemctl start docker`

## 3. Run docker compose

The directory consists of `docker-compose.yaml` which file will hold all the deatils about the chromaDB instance. This is used to start the chromaDB container

`docker-compose up -d`

## 5. Check the containers are running

Make sure the container are running. You will get a list of all the running containers.

`docker ps`

## 6. Verify everything

You can check if everything was setup correctly by sending an HTTP `GET` request to the folling endpoint

`curl http://localhost:8000/api/v1/heartbeat`

This should return a nanosecond heartbeat like below

`{"nanosecond heartbeat":1700043941276595546}`

# Setup Nemo English on CentOS

Speechbrain is the language identification model used to detect the language being spoken in the audiofile. We will be deploying speechbrain wrapped in a flask api with an endpoint `/transcribe_en` which is used to interact with the model.

## 1. Switch the directory

Change the directory to `nemo-en` in the `ats_scripts` directory

`cd nemo-en`

## 2. Start the docker engine

Start the docker engine if not already running

`sudo systemctl start docker`

## 3. Run docker compose

The directory consists of `docker-compose.yaml` which file will hold all the deatils about the nemo-en instance. This is used to start the nemo-en container

`docker-compose up -d`

## 5. Check the containers are running

Make sure the container are running. You will get a list of all the running containers.

`docker ps`

## 7. Usage

The nemo-en engine can be using by sending a post request like below

`curl -X POST -H "Content-Type: application/json" -d '{"audiofile":"https://omniglot.com/soundfiles/udhr/udhr_th.mp3"}' http://localhost:5002/transcribe_en`

Note: Replace the audiofile url in the request body with a valid audio url

# Setup Nemo Hindi on CentOS

Speechbrain is the language identification model used to detect the language being spoken in the audiofile. We will be deploying speechbrain wrapped in a flask api with an endpoint `/transcribe_hi` which is used to interact with the model.

## 1. Switch the directory

Change the directory to `nemo-hi` in the `ats_scripts` directory

`cd nemo-hi`

## 2. Start the docker engine

Start the docker engine if not already running

`sudo systemctl start docker`

## 3. Run docker compose

The directory consists of `docker-compose.yaml` which file will hold all the deatils about the nemo-hi instance. This is used to start the nemo-hi container

`docker-compose up -d`

## 5. Check the containers are running

Make sure the container are running. You will get a list of all the running containers.

`docker ps`

## 7. Usage

The nemo-hi engine can be using by sending a post request like below

`curl -X POST -H "Content-Type: application/json" -d '{"audiofile":"https://omniglot.com/soundfiles/udhr/udhr_th.mp3"}' http://localhost:5003/transcribe_hi`

Note: Replace the audiofile url in the request body with a valid audio url

# Setup Spacy on CentOS

Spacy is an open-source NLP library for efficiently processing and analyzing text data, offering pre-trained models for tasks like tokenization, part-of-speech tagging, and named entity recognition. We will be deploying spacy wrapped in a flask api with an endpoint `/get_entities` which is used to interact with the model.

## 1. Switch the directory

Change the directory to `spacy` in the `ats_scripts` directory

`cd spacy`

## 2. Start the docker engine

Start the docker engine if not already running

`sudo systemctl start docker`

## 3. Run docker compose

The directory consists of `docker-compose.yaml` which file will hold all the deatils about the spacy instance. This is used to start the spacy container

`docker-compose up -d`

## 5. Check the containers are running

Make sure the container are running. You will get a list of all the running containers.

`docker ps`

## 6. Verify everything

You can check if everything was setup correctly by sending an HTTP GET request to the folling endpoint

`curl http://localhost:5001/api_status`

## 7. Usage

The spacy engine can be using by sending a post request like below

`curl -X POST -H "Content-Type: application/json" -d '{"sentence": "John Doe is a man"}' http://localhost:5001/get_entities`

Note: Replace the `sentence` in the request body with a valid data

# Setup Speechbrain on CentOS

Speechbrain is the language identification model used to detect the language being spoken in the audiofile. We will be deploying speechbrain wrapped in a flask api with an endpoint `/predict_language` which is used to interact with the model.

## 1. Switch the directory

Change the directory to `speechbrain` in the `ats_scripts` directory

`cd speechbrain`

## 2. Start the docker engine

Start the docker engine if not already running

`sudo systemctl start docker`

## 3. Run docker compose

The directory consists of `docker-compose.yaml` which file will hold all the deatils about the speechbrain instance. This is used to start the speechbrain container

`docker-compose up -d`

## 5. Check the containers are running

Make sure the container are running. You will get a list of all the running containers.

`docker ps`

## 6. Verify if the database is running

You can check if everything was setup correctly by sending an HTTP GET request to the folling endpoint

`curl http://localhost:5000/api_status`

## 7. Usage

The speechbrain engine can be using by sending a post request like below

`curl -X POST -H "Content-Type: application/json" -d '{"filepath":"https://omniglot.com/soundfiles/udhr/udhr_th.mp3"}' http://localhost:5000/predict_language`

Note: Replace the filepath url in the request body with a valid audio url
