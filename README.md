# Document QA 
- This repository contains Python code to demonstrate Andes' ability to run Question Answering over documents
- Runs on python 3.10.9

## Setup
- Clone the repository
- Install docker
- Install docker-compose
- Replace your AWS access key and secret key in the docker-compose.yml file
- Execute the following commands:
``` 
cd ~/andes-backend
./run-server.sh
```

## Port mapping
- 8000: server
- 3000: graphana

## Starting Up
- `python run.py`
- `python run_workers.py`

## Redis Setup
- install redis
    `sudo apt-get install redis-server`
- start redis CLI / does not seems to work
    `rq worker --with-scheduler index_gen`


## Setup Graphana and Prometheus
- install graphana
    - https://grafana.com/grafana/download
- go to http://localhost:3000
- login with admin/admin
- add data source (prometheus)
    - http://localhost:9090
- add dashboard
