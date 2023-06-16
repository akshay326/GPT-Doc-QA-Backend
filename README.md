# andes-backend

- runs on python 3.10.9
- python -m andes.api

http://13.52.22.190:8000/test


## Redis Setup
- install redis
    sudo apt-get install redis-server
- start redis CLI / does not seems to work
    rq worker --with-scheduler index_gen
- python run_workers.py