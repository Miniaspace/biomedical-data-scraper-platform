# Architecture Design

This document provides a detailed overview of the system architecture for the Biomedical Data Scraper Platform.

## 1. Guiding Principles

The architecture is designed based on the following core principles:

- **Scalability**: The system must be able to handle a growing number of data sources and increasing data volume without significant redesign.
- **Extensibility**: Adding new data sources (platforms) should be simple, fast, and require minimal boilerplate code.
- **Reliability**: The system must be robust, with built-in error handling, retries, and fault tolerance.
- **Maintainability**: Code should be modular, well-documented, and easy to understand and modify.
- **Observability**: The system must provide clear insights into its operational status through comprehensive logging, monitoring, and alerting.

## 2. System Components

The platform is composed of several key components, each with a distinct responsibility:

![System Architecture Diagram](architecture.png)

### 2.1. Orchestration Layer (Apache Airflow)

- **Responsibility**: Manages the entire lifecycle of scraping tasks, including scheduling, execution, monitoring, and retries.
- **Key Feature**: A **Dynamic DAG Factory** (`dags/platform_dag_factory.py`) automatically generates a DAG for each platform defined in `config/platforms.yaml`. This eliminates manual DAG creation and ensures consistency.
- **Workflow**: Each DAG consists of several tasks: running the spider, validating the data, exporting to different formats, and sending notifications.

### 2.2. Scraping Layer (Scrapy)

- **Responsibility**: Executes the actual web scraping logic to extract data from target websites.
- **Key Feature**: A **Base Spider Template** (`common/base_spider.py`) provides all common functionality (authentication, rate limiting, logging). Platform-specific spiders (e.g., `spiders/biolincc_spider.py`) inherit from this base class and only need to implement the parsing logic.
- **Extensibility**: To add a new platform, a developer simply creates a new spider class inheriting from `BaseSpider`.

### 2.3. Core Infrastructure (Common Modules)

This is a collection of shared services that support the entire platform:

- **Authentication Manager (`common/auth/auth_manager.py`)**: Securely stores and retrieves credentials for all platforms. Supports encrypted storage.
- **Data Pipeline (`common/pipeline/data_pipeline.py`)**: Handles post-scraping processing, including data validation, transformation, deduplication, and storage.
- **Monitoring & Alerting (`common/monitor/`)**: (Future implementation) Integrates with Prometheus and Grafana for monitoring and sends alerts via email or Slack.

### 2.4. Data Storage Layer

- **PostgreSQL**: Serves as the backend for Apache Airflow, storing metadata about DAGs, task instances, and connections.
- **Redis**: Acts as the message broker for the Celery executor (if used for distributed scraping) and can be used for caching.
- **MinIO (S3-compatible)**: An object storage service used to store large data files, such as raw HTML, PDFs, images, and processed datasets.
- **Local Filesystem (`/data`)**: Used for storing raw JSONL data, logs, and temporary files. This directory is mounted as a volume in Docker.

### 2.5. Containerization Layer (Docker)

- **Responsibility**: Packages the entire application and its dependencies into portable, isolated containers.
- **Key Feature**: A `docker-compose.yml` file orchestrates all services (Airflow, Postgres, Redis, MinIO), allowing for a one-command setup (`docker-compose up`).
- **Custom Image**: A `Dockerfile` is used to build a custom Airflow image that includes all project dependencies and configurations.

## 3. Data Flow

The data flows through the system as follows:

1.  **Scheduling**: The Airflow Scheduler triggers a platform-specific DAG based on its cron schedule.
2.  **Task Execution**: Airflow's executor picks up the task and executes the `run_spider` Python function.
3.  **Spider Invocation**: The `run_spider` function invokes the appropriate Scrapy spider via a command-line interface.
4.  **Authentication**: The spider's `BaseSpider` parent class requests credentials from the `AuthManager` if authentication is required.
5.  **Scraping**: The spider sends HTTP requests to the target platform, respecting rate limits and handling retries.
6.  **Parsing**: The spider parses the HTML responses and extracts data items.
7.  **Pipeline Processing**: Each extracted item is passed to the Scrapy `DataPipeline`.
8.  **Validation & Transformation**: The pipeline validates the item, enriches it with metadata, and calculates a quality score.
9.  **Storage**: The processed item is appended to a JSONL file in the `data/raw/{platform_name}/` directory.
10. **Post-Processing**: After the spider finishes, subsequent Airflow tasks are triggered to validate the entire dataset, export it to CSV, and send a completion notification.

## 4. Extensibility in Practice

Adding a new platform, `new_platform`, involves:

1.  **Creating `spiders/new_platform_spider.py`**: Inherit from `BaseSpider` and implement `parse_list_page` and `parse_detail_page`.
2.  **Adding an entry to `config/platforms.yaml`**: Define the platform's name, URL, schedule, etc.
3.  **Adding credentials to `config/credentials.yaml`**: If `auth_required` is true.
4.  **Restarting Airflow**: The DAG factory will automatically detect the new configuration and create a `scrape_new_platform` DAG.

This design minimizes developer effort and ensures that the core system remains stable and untouched, fulfilling the key principles of extensibility and maintainability.
