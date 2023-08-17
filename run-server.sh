# stop redis on host if running
sudo systemctl status redis

# first stop existing docker compose containers
docker compose down

# then build again
docker compose build

# then run using docker-compose.yml
docker compose up
