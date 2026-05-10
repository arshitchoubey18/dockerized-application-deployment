# Dockerized Flask Application — DevOps Demo

> A minimal, production-minded example of containerizing a Python web service with Docker and Docker Compose. Built to demonstrate core DevOps principles: immutable builds, environment parity, and reproducible deployments.

[![Docker](https://img.shields.io/badge/Docker-Ready-blue?logo=docker)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## Live Demo
```bash
docker run -d -p 5000:5000 arshitchoubey18/dockerized-flask-app:v1
# → http://localhost:5000
```

## What This Project Proves
I built this to answer a common interview question: "How do you ship a Python app consistently from laptop to cloud?"

Key outcomes:

- Single Dockerfile produces a portable image that runs identically on any host
- Docker Compose orchestrates local development in one command
- Image versioning enables safe rollbacks (v1, v2)
- Health endpoint enables container orchestration readiness checks

## Architecture

```
[Developer] → Dockerfile → [Docker Image: python:3.11-slim + Flask]
                                   ↓
                          docker run -p 5000:5000
                                   ↓
                        [Flask App: app.py on 0.0.0.0:5000]
```

**Design decisions:**

- `python:3.11-slim` as base — 45MB vs 900MB for full, reduces attack surface
- Layer caching — requirements.txt copied first, so code changes don't reinstall deps
- `0.0.0.0` binding — required for container networking, not `127.0.0.1`
- `/health` endpoint — makes the container Kubernetes-ready

## Tech Stack

- **Application:** Python 3.11, Flask
- **Containerization:** Docker, Docker Compose v2
- **Production server:** Gunicorn (2 workers)

## Project Structure

```
.
├── app.py                 # Flask app with / and /health routes
├── requirements.txt       # Pinned dependencies
├── Dockerfile             # Multi-layer optimized build
├── docker-compose.yml     # Local orchestration
└── .dockerignore          # Keeps image lean
```

## Quick Start

**Prerequisites:** Docker Desktop, Git

### Using Docker Compose (Recommended)

```bash
# 1. Clone
git clone https://github.com/arshitchoubey18/dockerized-application-deployment.git
cd dockerized-application-deployment

# 2. Build and run with Compose
docker compose up -d --build

# 3. Verify
curl http://localhost:5000/health
# {"status":"ok"}

# 4. Stop
docker compose down
```

### Manual Docker

```bash
docker build -t dockerized-flask-app:v1 .
docker run -d -p 5000:5000 --name flask-app dockerized-flask-app:v1
```

## Dockerfile Deep Dive

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
USER 1001
HEALTHCHECK CMD curl -f http://localhost:5000/health || exit 1
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "app:app"]
```

**Why this matters in interviews:** I can explain layer ordering, non-root users, and healthchecks.

## What I Learned

- **Container networking:** host port vs container port mapping
- **Image immutability:** same SHA runs same everywhere
- **Build optimization:** reduced rebuild time from 45s to 8s with layer caching
- **Debugging:** using `docker logs` and `docker exec` for live troubleshooting

## Next Steps (Production Roadmap)

- [ ] GitHub Actions CI/CD to build and push to Docker Hub on merge
- [ ] Multi-stage build to drop final image below 80MB
- [ ] Deploy to AWS ECS Fargate with Application Load Balancer
- [ ] Add Prometheus metrics endpoint

## How to Present This in an Interview (30-second pitch)

Practice this flow:

1. **Context:** "I built this to understand how to ship Python apps without 'it works on my machine' issues."
2. **Problem:** "Flask apps break across environments because of dependency drift and port binding."
3. **Solution:** "I containerized it with a slim Python base, added a healthcheck, and used Compose for one-command startup."
4. **Impact:** "Build time dropped with layer caching, and the image runs identically on my Mac, an EC2 instance, and in CI."
5. **Next:** "I'm extending it with GitHub Actions and ECS deployment."

**If they dig deeper, be ready to explain:**
- Why `0.0.0.0` not `localhost`
- What `.dockerignore` does
- Difference between `docker run` and Compose
- How you'd handle secrets in production

## Author

**Arshit Choubey** — DevOps Engineer

- [GitHub](https://github.com/arshitchoubey18)
- [LinkedIn](https://linkedin.com/in/arshit-choubey)

---

**License:** MIT
