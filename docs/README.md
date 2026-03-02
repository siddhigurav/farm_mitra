# Running the Intelligent Insect & Animal Monitoring System

This document explains how to run the system using Docker and Docker Compose.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## 1. Configure Environment Variables

Before running the system, you need to set up your environment variables.

1.  Navigate to the `deployment/config` directory.
2.  Make a copy of the `.env.example` file and rename it to `.env`.
3.  Open the `.env` file and fill in your MySQL credentials and any other API keys you might be using.

## 2. Build and Run the System

Once your `.env` file is configured, you can start the entire application stack with a single command.

1.  Open a terminal in the `deployment` directory.
2.  Run the following command:

    ```bash
    docker-compose up --build
    ```

This command will:

-   Build the Docker images for the backend and frontend services.
-   Start the containers for the backend, frontend, and MySQL database.

## 3. Accessing the Application

-   **Frontend (React App):** Open your web browser and navigate to `http://localhost`.
-   **Backend (FastAPI):** The API will be available at `http://localhost:8000`.

## 4. Stopping the System

To stop the running containers, press `Ctrl+C` in the terminal where `docker-compose` is running. To remove the containers, you can run:

```bash
docker-compose down
```
