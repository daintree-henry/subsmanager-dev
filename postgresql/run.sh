docker rm -f subsmanager-postgres
docker build -t subsmanager-postgres . --no-cache
docker run --name subsmanager-postgres -d -p 5432:5432 subsmanager-postgres