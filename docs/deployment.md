# Deployment Guide

This guide covers deploying the Biomedical Data Scraper Platform to a production environment.

## 1. Prerequisites

- A server (or cluster) with Docker and Docker Compose installed.
- A domain name (optional, for secure access).
- A configured SMTP server for email notifications (optional).

## 2. Environment Configuration

The most critical step for production deployment is correctly configuring the environment variables.

1.  **Copy the example file**:

    ```bash
    cp .env.example .env
    ```

2.  **Edit the `.env` file** and set the following production values:

    -   `ENVIRONMENT`: Set to `production`.
    -   `AIRFLOW__WEBSERVER__SECRET_KEY`: **MUST** be changed to a long, random string.
    -   `CREDENTIAL_ENCRYPTION_KEY`: **MUST** be set. Generate a new key with `python common/auth/auth_manager.py` and store it securely.
    -   `POSTGRES_PASSWORD`, `MINIO_ROOT_PASSWORD`: Change these to strong, secure passwords.
    -   `SMTP_*`: Configure your SMTP server settings for email alerts.
    -   `SLACK_WEBHOOK_URL`: Configure your Slack webhook for notifications.

## 3. Production Docker Compose

For production, it is recommended to use a slightly modified `docker-compose.prod.yml` that might include:

-   Persistent volumes mapped to durable storage (e.g., NFS, cloud storage).
-   Integration with a reverse proxy like Nginx or Traefik for SSL termination.
-   Increased resource limits for containers.

**Example `docker-compose.prod.yml` (partial):**

```yaml
services:
  postgres:
    volumes:
      - /mnt/persistent_storage/postgres:/var/lib/postgresql/data
  minio:
    volumes:
      - /mnt/persistent_storage/minio:/data
  # ... other services
```

## 4. Deployment Steps

1.  **Clone the repository** on the production server:

    ```bash
    git clone https://github.com/yourusername/biomedical-data-scraper-platform.git
    cd biomedical-data-scraper-platform
    ```

2.  **Create and configure the `.env` file** as described above.

3.  **Create and configure `config/credentials.yaml`**: Add the actual production credentials for all required platforms. Ensure this file is encrypted if `CREDENTIAL_ENCRYPTION_KEY` is set.

4.  **Build and start the services**:

    ```bash
    docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
    ```

    This command merges the base and production compose files, builds the custom Airflow image, and starts all services in detached mode.

5.  **Verify the deployment**:

    -   Check the status of all containers: `docker-compose ps`
    -   Check the logs for any errors: `docker-compose logs -f`
    -   Access the Airflow UI at your server's IP/domain on port 8080.

## 5. Security Best Practices

-   **Firewall**: Restrict access to ports. Only expose ports 80/443 (via a reverse proxy) to the public internet.
-   **Secrets Management**: For higher security, consider using a dedicated secrets manager like HashiCorp Vault or AWS Secrets Manager instead of environment variables.
-   **Regular Updates**: Periodically update the base Docker images and Python dependencies to patch security vulnerabilities.
-   **Backups**: Regularly back up the PostgreSQL database and the MinIO data volumes.

## 6. Scaling

If you need to scale the platform to handle more concurrent tasks, you can switch to the `CeleryExecutor`.

1.  **Update `.env`**:

    ```
    AIRFLOW__CORE__EXECUTOR=CeleryExecutor
    ```

2.  **Add Celery workers** to your `docker-compose.yml`:

    ```yaml
    services:
      airflow-worker:
        <<: *airflow-common
        command: celery worker
        restart: always
        depends_on:
          <<: *airflow-common-depends-on
          airflow-init:
            condition: service_completed_successfully
    ```

3.  **Scale the workers**:

    ```bash
    docker-compose up -d --scale airflow-worker=5
    ```

    This will start 5 Celery workers to execute tasks in parallel.

## 7. Monitoring

-   **Airflow UI**: The primary tool for monitoring DAG and task status.
-   **Logs**: All logs are stored in the `logs` directory, which is mounted as a volume. You can also view logs directly in the Airflow UI.
-   **Prometheus/Grafana**: (Future implementation) The architecture is designed to be scraped by Prometheus. You can set up a separate monitoring stack to collect metrics from Airflow and other services.
