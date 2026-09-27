# Installation and Deployment Guide

This guide outlines the step-by-step instructions for setting up, building, and running the application for both local development and Docker-based environments.

## Local Development Setup (Without Docker)

1. **Clone the repository and navigate to the project root.**
2. **Install dependencies:**
   ```bash
   npm install
   ```
3. **Configure Environment Variables:**
   Create a `.env` file in the project root based on your environment requirements (e.g., `PORT=3000`, `NODE_ENV=development`).
4. **Run the application:**
   ```bash
   npm run dev
   ```

## Docker & Docker Compose Setup

The application includes a complete container configuration via `Dockerfile` and `docker-compose.yml`.

### 1. Environment Variables
Ensure a `.env` file exists in the project root if required by your configuration, or rely on defaults provided in `docker-compose.yml`.

### 2. Build and Run Containers
To build the images from scratch and start all services in detached mode:
```bash
docker-compose up --build -d
```

### 3. Verification
Verify that the containers are running correctly:
```bash
docker-compose ps
```

### 4. Stopping the Application
To stop and remove containers, networks, and volumes created by Compose:
```bash
docker-compose down
```
