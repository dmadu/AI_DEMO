# Installation Guide

This guide provides step-by-step instructions for setting up the development environment and running the application using Docker Compose.

## Prerequisites

Before you begin, ensure you have installed:
- [Docker](https://docs.docker.com/get-docker/) (v20.10 or higher recommended)
- [Docker Compose](https://docs.docker.com/compose/install/) (v2.0 or higher recommended)
- Git

## Step 1: Clone the Repository

Clone the repository to your local machine:

```bash
git clone <repository-url>
cd project_24
```

## Step 2: Environment Configuration

The application relies on environment variables for configuration. A template file `.env.example` is provided in the project root.

Create your local `.env` file:

```bash
cp .env.example .env
```

Open `.env` in your preferred text editor and adjust any configuration values (such as port numbers, database URLs, or logging levels) to suit your environment.

## Step 3: Run with Docker Compose

Build and start the application containers in detached mode or attached mode to view logs:

```bash
# Build and run containers
docker-compose up --build
```

If you prefer running in the background:

```bash
docker-compose up --build -d
```

## Step 4: Verify Installation

Once the containers are running, you can verify the health of the application by checking the Docker container status and accessing the health check endpoint:

```bash
docker-compose ps
```

Access the application endpoint via `http://localhost:<PORT>` (refer to your `.env` configuration for the active port).

## Stopping the Application

To stop the running containers, execute:

```bash
docker-compose down
```