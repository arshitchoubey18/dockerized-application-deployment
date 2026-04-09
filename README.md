# Dockerized Application Deployment

A Flask application containerized using Docker and managed with Docker Compose.

## Tech Stack
- Python
- Flask
- Docker
- Docker Compose
- Nginx
- Redis

## Project Structure
.
├── app.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .env
├── nginx.conf
└── README.md

## Prerequisites
- Docker installed
- Docker Compose installed

## Build Docker Image
docker build -t dockerized-flask-app:v1 .

## Run with Docker
docker run -d -p 5000:5000 --name flask-app dockerized-flask-app:v1

## Run with Docker Compose
docker compose up --build -d

## Stop Services
docker compose down

## View Logs
docker compose logs -f

## Endpoints
- App: http://localhost
- Health: http://localhost/health

## Cleanup
docker compose down -v
docker system prune -f
