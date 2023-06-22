# andes-backend
- runs on python 3.10.9
- http://13.52.22.190:8000/test
- keys saved at `/home/ubuntu/andes-backend/.env`


## port mapping
- 8000: server
- 3000: graphana

## Starting Up
- python run.py
- python run_workers.py


## Redis Setup
- install redis
    sudo apt-get install redis-server
- start redis CLI / does not seems to work
    rq worker --with-scheduler index_gen


## Setup Graphana and Prometheus
- install graphana
    - https://grafana.com/grafana/download
- go to http://localhost:3000
- login with admin/admin
- add data source (prometheus)
    - http://localhost:9090
- add dashboard