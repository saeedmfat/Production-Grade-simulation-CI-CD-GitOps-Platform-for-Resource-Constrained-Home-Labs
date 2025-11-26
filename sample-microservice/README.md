# Sample Microservice

A lightweight FastAPI microservice for CI/CD and GitOps demonstrations.

## Features

- Health check endpoint (`/health`)
- Echo service (`/echo`)
- Service information (`/info`)
- Unit tests with pytest
- Docker containerization
- Multi-stage Docker build

## Local Development

### Run with Docker Compose
```bash
docker-compose up --build
