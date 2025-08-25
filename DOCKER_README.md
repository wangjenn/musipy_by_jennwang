# 🐳 MusiPy Docker Deployment Guide

This guide will help you deploy MusiPy using Docker for a fully portable and reproducible setup.

## 🚀 Quick Start

### Option 1: Using Docker Compose (Recommended)

```bash
# Build and run the application
docker-compose up --build

# Run in background
docker-compose up -d --build

# Stop the application
docker-compose down
```

### Option 2: Using Docker directly

```bash
# Build the image
docker build -t musipy .

# Run the container
docker run -p 9000:9000 musipy

# Run in background
docker run -d -p 9000:9000 --name musipy-app musipy
```

## 📁 Project Structure

```
musipy_by_jennwang/
├── app/                    # Flask application
├── data/                   # CSV data files
├── models/                 # ML model files
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose configuration
├── requirements.txt       # Python dependencies
└── run_production.py      # Production entry point
```

## 🔧 Configuration

### Environment Variables

You can customize the application by setting environment variables:

```bash
# In docker-compose.yml
environment:
  - FLASK_ENV=production
  - PYTHONUNBUFFERED=1
```

### Port Configuration

The application runs on port 9000 by default. You can change this in `docker-compose.yml`:

```yaml
ports:
  - "8080:9000"  # Map host port 8080 to container port 9000
```

## 🏥 Health Checks

The application includes health checks to ensure it's running properly:

```bash
# Check container health
docker ps

# View health check logs
docker logs musipy-app
```

## 📊 Monitoring

### View logs
```bash
# Docker Compose
docker-compose logs -f

# Docker
docker logs -f musipy-app
```

### Access the application
- **URL**: http://localhost:9000
- **Health Check**: http://localhost:9000/

## 🔄 Updates

To update the application:

```bash
# Stop the current container
docker-compose down

# Rebuild and start
docker-compose up --build -d
```

## 🛠️ Development

For development, you can mount the source code as a volume:

```yaml
# In docker-compose.yml
volumes:
  - .:/app
  - ./data:/app/data:ro
  - ./models:/app/models:ro
```

## 🐛 Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # Check what's using port 9000
   lsof -i :9000
   
   # Change port in docker-compose.yml
   ports:
     - "9001:9000"
   ```

2. **Permission issues**
   ```bash
   # Fix file permissions
   sudo chown -R $USER:$USER .
   ```

3. **Memory issues**
   ```bash
   # Increase Docker memory limit
   # In Docker Desktop settings
   ```

### Logs and Debugging

```bash
# View application logs
docker-compose logs musipy

# Access container shell
docker-compose exec musipy bash

# Check container resources
docker stats
```

## 🔒 Security

The Docker setup includes several security features:

- Non-root user execution
- Read-only data mounts
- Health checks
- Resource limits

## 📈 Production Deployment

For production deployment, consider:

1. **Reverse Proxy**: Use nginx or Apache
2. **SSL/TLS**: Add HTTPS support
3. **Load Balancing**: Use multiple containers
4. **Monitoring**: Add Prometheus/Grafana
5. **Backup**: Regular data backups

Example production docker-compose:

```yaml
version: '3.8'
services:
  musipy:
    build: .
    ports:
      - "9000:9000"
    environment:
      - FLASK_ENV=production
    restart: unless-stopped
    deploy:
      resources:
        limits:
          memory: 2G
        reservations:
          memory: 1G
```

## 🎯 Benefits of Docker Deployment

✅ **Portability**: Run anywhere Docker is available  
✅ **Reproducibility**: Same environment every time  
✅ **Isolation**: No conflicts with system dependencies  
✅ **Scalability**: Easy to deploy multiple instances  
✅ **Security**: Isolated execution environment  
✅ **Versioning**: Easy to rollback to previous versions  
