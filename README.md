# Biomedical Data Scraper Platform

> A scalable, AI-powered, production-ready data scraping platform for biomedical research databases. Built with Apache Airflow + Scrapy.

## 🌟 Overview

This platform is designed as a **universal, extensible data acquisition infrastructure** that can efficiently scrape data from multiple biomedical research platforms. It separates core infrastructure from platform-specific adapters, enabling rapid integration of new data sources with minimal development effort.

### Key Features

- **🔧 Modular Architecture**: Separation of core infrastructure and platform adapters
- **🚀 Scalable Design**: Distributed task execution with Redis and Celery
- **🤖 AI-Assisted Development**: GPT-4 powered code generation for new adapters
- **🔐 Unified Authentication**: Centralized credential management for all platforms
- **📊 Comprehensive Monitoring**: Real-time dashboards and alerting system
- **🔄 Auto-Recovery**: Intelligent retry mechanisms and error handling
- **📦 Data Quality Assurance**: Built-in validation and deduplication
- **🐳 Docker Ready**: Complete containerization for easy deployment

## 📋 Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Apache Airflow                           │
│              (Orchestration & Scheduling)                   │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   Core Infrastructure                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Auth Mgr   │  │  Data Pipeline│  │   Monitor    │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              Platform Adapters (Scrapy Spiders)             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  BioLINCC    │  │   OpenICPSR  │  │   YODA       │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    Data Storage Layer                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  PostgreSQL  │  │    MinIO     │  │    Redis     │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

We provide two running modes: **Local Direct Execution** (no Docker required, suitable for quick testing and development) and **Docker Containerized Execution** (recommended for production environments).

### Local Direct Execution (No Docker)

1. **Clone the repository**
```bash
git clone https://github.com/Miniaspace/biomedical-data-scraper-platform.git
cd biomedical-data-scraper-platform
```

2. **Install dependencies**
```bash
# Install dependencies for local execution
pip install -r requirements-local.txt
```

3. **Run the scraper**
```bash
# List all available platforms
python run_local.py --list

# Run a single platform (e.g., Kids First)
python run_local.py --platform kidsfirst

# Run all enabled platforms
python run_local.py --platform all
```

For a detailed guide, please see [QUICKSTART.md](QUICKSTART.md).

### Docker Containerized Execution (Recommended for Production)

1. **Clone the repository**
```bash
git clone https://github.com/Miniaspace/biomedical-data-scraper-platform.git
cd biomedical-data-scraper-platform
```

2. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your configurations
```

3. **Start the platform**
```bash
docker-compose up -d
```

4. **Access Airflow UI**
```
URL: http://localhost:8080
Username: airflow
Password: airflow
```

## 📚 Directory Structure

```
biomedical-data-scraper-platform/
├── dags/                      # Airflow DAG definitions
│   ├── platform_dag_factory.py    # Dynamic DAG generator
│   └── example_platform_dag.py    # Example DAG
├── spiders/                   # Scrapy spiders (Platform Adapters)
│   ├── base_spider.py             # Base spider template
│   ├── biolincc_spider.py         # BioLINCC adapter
│   └── openicpsr_spider.py        # OpenICPSR adapter
├── common/                    # Core infrastructure modules
│   ├── auth/                      # Authentication management
│   ├── pipeline/                  # Data processing pipelines
│   ├── monitor/                   # Monitoring and alerting
│   └── utils/                     # Utility functions
├── config/                    # Configuration files
│   ├── platforms.yaml             # Platform configurations
│   ├── credentials.yaml.example   # Credential template
│   └── airflow.cfg                # Airflow configuration
├── scripts/                   # Deployment and utility scripts
│   ├── setup.sh                   # Initial setup script
│   └── add_platform.py            # Add new platform script
├── tests/                     # Unit and integration tests
├── docs/                      # Documentation
│   ├── architecture.md            # Architecture design
│   ├── adding_new_platform.md     # Guide for adding platforms
│   └── deployment.md              # Deployment guide
├── data/                      # Data storage (gitignored)
│   ├── raw/                       # Raw scraped data
│   ├── processed/                 # Processed data
│   └── logs/                      # Application logs
├── docker-compose.yml         # Docker orchestration
├── Dockerfile                 # Custom Airflow image
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## 🔧 Adding a New Platform

Adding a new data source takes only **3 simple steps**:

### Step 1: Create Spider Adapter

```python
# spiders/new_platform_spider.py
from common.base_spider import BaseSpider

class NewPlatformSpider(BaseSpider):
    name = 'new_platform'
    
    def parse_list_page(self, response):
        # Extract detail page links
        pass
    
    def parse_detail_page(self, response):
        # Extract target data fields
        pass
```

### Step 2: Add Configuration

```yaml
# config/platforms.yaml
new_platform:
  name: "New Platform"
  base_url: "https://new-platform.com"
  spider_class: "NewPlatformSpider"
  schedule: "0 2 * * *"  # Daily at 2 AM
```

### Step 3: Deploy

```bash
python scripts/add_platform.py new_platform
```

That's it! The platform will automatically create a DAG and start scraping.

## 📖 Documentation

- [Architecture Design](docs/architecture.md) - Detailed system architecture
- [Adding New Platforms](docs/adding_new_platform.md) - Step-by-step guide
- [Deployment Guide](docs/deployment.md) - Production deployment
- [API Reference](docs/api_reference.md) - Core module APIs
- [Troubleshooting](docs/troubleshooting.md) - Common issues and solutions

## 🛠 Technology Stack

| Component | Technology |
|-----------|-----------|
| **Orchestration** | Apache Airflow 2.8+ |
| **Scraping** | Scrapy 2.11+ |
| **Task Queue** | Redis + Celery |
| **Database** | PostgreSQL 15+ |
| **Object Storage** | MinIO |
| **Containerization** | Docker + Docker Compose |
| **Monitoring** | Prometheus + Grafana |
| **Dynamic Pages** | Playwright |
| **AI Assistant** | OpenAI GPT-4 |

## 📊 Current Platform Coverage

This platform currently supports **75 biomedical research databases**, including:

- BioLINCC (NHLBI)
- OpenICPSR
- YODA Project
- Vivli
- NCBI dbGaP
- And 70+ more...

See [PLATFORMS.md](docs/PLATFORMS.md) for the complete list.

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Apache Airflow](https://airflow.apache.org/)
- Powered by [Scrapy](https://scrapy.org/)
- Inspired by the open-source community

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**Made with ❤️ for the biomedical research community**
