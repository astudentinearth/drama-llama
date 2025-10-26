# Docker Setup Guide

This guide explains how to run the Drama Llama AI service using Docker.

## Prerequisites

- Docker Engine 20.10 or later
- Docker Compose 2.0 or later

## Quick Start

### 1. Environment Configuration

Copy the example environment file and configure it:

```bash
cp .env.example .env
```

Edit `.env` and set your actual values:

- `GROQ_API_KEY`: Your GROQ API key
- `API_KEY_SECRET`: A secure secret key for API authentication
- `POSTGRES_PASSWORD`: A strong password for PostgreSQL (for Docker deployment)

### 2. Build and Run with Docker Compose

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# View logs for specific service
docker-compose logs -f ai_service
```

### 3. Verify the Setup

Check the health endpoint:

```bash
curl http://localhost:8001/health
```

You should see a response like:

```json
{
  "status": "ok",
  "database": "connected",
  "error": null
}
```

## Services

The Docker setup includes:

- **ai_service**: FastAPI application (port 8001)
- **postgres**: PostgreSQL database (port 5432)

## Database Management

### Initialize Database

The database will be automatically initialized on first run. To manually trigger initialization:

```bash
curl http://localhost:8001/health
```

### Access PostgreSQL

```bash
# Using docker-compose
docker-compose exec postgres psql -U postgres -d dramallama_ai

# Using docker directly
docker exec -it dramallama_postgres psql -U postgres -d dramallama_ai
```

### Database Migrations

If you need to run Alembic migrations:

```bash
docker-compose exec ai_service alembic upgrade head
```

## Development Mode

For development with hot reload:

1. Uncomment the volume mount in `docker-compose.yml`:

   ```yaml
   volumes:
     - .:/app
   ```

2. Set `API_RELOAD=True` in your `.env` file

3. Restart the service:
   ```bash
   docker-compose restart ai_service
   ```

## Useful Commands

### Stop Services

```bash
docker-compose down
```

### Stop and Remove Volumes (⚠️ This will delete your database)

```bash
docker-compose down -v
```

### Rebuild Services

```bash
docker-compose up -d --build
```

### View Service Status

```bash
docker-compose ps
```

### Execute Commands in Container

```bash
# Open a shell
docker-compose exec ai_service /bin/bash

# Run Python script
docker-compose exec ai_service python scripts/check_ollama.py
```

### View Resource Usage

```bash
docker stats
```

## Production Deployment

For production deployment:

1. **Set secure credentials** in `.env`:

   - Strong `POSTGRES_PASSWORD`
   - Secure `API_KEY_SECRET`
   - Never commit `.env` to version control

2. **Disable API reload**:

   ```
   API_RELOAD=False
   ```

3. **Configure proper logging**:

   ```
   LOG_LEVEL=WARNING
   ```

4. **Use production-grade PostgreSQL**:

   - Consider using a managed database service
   - Set up proper backups
   - Configure connection pooling

5. **Add reverse proxy** (nginx/traefik) for:

   - SSL/TLS termination
   - Load balancing
   - Rate limiting

6. **Security considerations**:
   - Run containers as non-root user (already configured)
   - Use Docker secrets for sensitive data
   - Keep base images updated
   - Scan images for vulnerabilities

## Troubleshooting

### Port Already in Use

If ports 8001 or 5432 are already in use:

1. Change the port mapping in `docker-compose.yml`:

   ```yaml
   ports:
     - "8002:8001" # Change external port
   ```

2. Or stop the conflicting service

### Database Connection Issues

Check if PostgreSQL is healthy:

```bash
docker-compose ps postgres
docker-compose logs postgres
```

### Container Logs

View detailed logs:

```bash
docker-compose logs --tail=100 ai_service
```

### Reset Everything

To start fresh:

```bash
docker-compose down -v
docker-compose up -d --build
```

## Network Configuration

Services communicate on the `dramallama_network` bridge network:

- Services can reach each other using service names as hostnames
- External access is controlled via port mappings

## Volume Management

### PostgreSQL Data

Data is persisted in the `postgres_data` volume:

```bash
# Backup database
docker-compose exec postgres pg_dump -U postgres dramallama_ai > backup.sql

# Restore database
docker-compose exec -T postgres psql -U postgres dramallama_ai < backup.sql
```

### Prompt Files

The `prompts/` directory is mounted into the container, allowing you to update prompts without rebuilding.

## Health Checks

The AI service includes a health check that runs every 30 seconds. You can view health status:

```bash
docker inspect dramallama_ai | grep -A 10 Health
```

## Support

For issues or questions:

1. Check the logs: `docker-compose logs`
2. Verify environment variables: `docker-compose config`
3. Test individual services: `docker-compose up postgres` then `docker-compose up ai_service`
