# MusicLibrary
An app to store an individual's data on their physical music library

To run program with docker:
docker-compose up -d
docker attach vinyl_vault-container

If container already exists:
docker start -ai vinyl_vault-container
docker stop vinyl_vault-container

docker pull conman4260/vinyl_vault:latest
docker run -it conman4260/vinyl_vault:latest

Persistent files:
docker run -it -v $(pwd)/codebase:/app/codebase conman4260/vinyl_vault:latest