"""
Platform DAG Factory

Dynamically generates Airflow DAGs for each configured platform.
This eliminates the need to manually create DAG files for each platform.
"""

import yaml
from datetime import datetime, timedelta
from pathlib import Path
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
import logging


# Load platform configurations
CONFIG_PATH = Path(__file__).parent.parent / "config" / "platforms.yaml"

def load_platform_configs():
    """Load platform configurations from YAML file."""
    try:
        with open(CONFIG_PATH, 'r') as f:
            return yaml.safe_load(f) or {}
    except Exception as e:
        logging.error(f"Failed to load platform configs: {e}")
        return {}


def run_spider(platform_name: str, **context):
    """
    Execute a Scrapy spider for a specific platform.
    
    Args:
        platform_name: Name of the platform to scrape
        context: Airflow context
    """
    import subprocess
    import sys
    
    # Get execution date from context
    execution_date = context['execution_date'].strftime('%Y-%m-%d')
    
    logging.info(f"Starting spider for platform: {platform_name}")
    logging.info(f"Execution date: {execution_date}")
    
    # Build scrapy command
    spider_module = f"spiders.{platform_name}_spider"
    cmd = [
        'scrapy', 'runspider',
        f'{spider_module}.py',
        '-a', f'platform={platform_name}',
        '-a', f'execution_date={execution_date}',
        '--logfile', f'data/logs/{platform_name}_{execution_date}.log',
    ]
    
    try:
        # Run spider
        result = subprocess.run(
            cmd,
            check=True,
            capture_output=True,
            text=True
        )
        
        logging.info(f"Spider completed successfully: {platform_name}")
        logging.info(f"Output: {result.stdout}")
        
        return {
            'status': 'success',
            'platform': platform_name,
            'execution_date': execution_date,
        }
        
    except subprocess.CalledProcessError as e:
        logging.error(f"Spider failed: {platform_name}")
        logging.error(f"Error: {e.stderr}")
        raise


def validate_data(platform_name: str, **context):
    """
    Validate scraped data quality.
    
    Args:
        platform_name: Name of the platform
        context: Airflow context
    """
    import json
    from pathlib import Path
    
    execution_date = context['execution_date'].strftime('%Y%m%d')
    data_file = Path(f'data/raw/{platform_name}/{platform_name}_{execution_date}.jsonl')
    
    if not data_file.exists():
        logging.warning(f"No data file found: {data_file}")
        return {'status': 'no_data', 'count': 0}
    
    # Count records and check quality
    record_count = 0
    quality_scores = []
    
    try:
        with open(data_file, 'r') as f:
            for line in f:
                record = json.loads(line)
                record_count += 1
                quality_scores.append(record.get('quality_score', 0))
        
        avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0
        
        logging.info(f"Validation results for {platform_name}:")
        logging.info(f"  Records: {record_count}")
        logging.info(f"  Avg quality score: {avg_quality:.2f}")
        
        return {
            'status': 'success',
            'count': record_count,
            'avg_quality': avg_quality,
        }
        
    except Exception as e:
        logging.error(f"Validation failed: {e}")
        raise


def send_notification(platform_name: str, **context):
    """
    Send notification about scraping completion.
    
    Args:
        platform_name: Name of the platform
        context: Airflow context
    """
    # Get results from previous tasks
    ti = context['ti']
    spider_result = ti.xcom_pull(task_ids=f'run_spider_{platform_name}')
    validation_result = ti.xcom_pull(task_ids=f'validate_data_{platform_name}')
    
    logging.info(f"Scraping completed for {platform_name}")
    logging.info(f"Spider result: {spider_result}")
    logging.info(f"Validation result: {validation_result}")
    
    # Here you can add email/Slack/webhook notifications
    # For now, just log the results
    
    return {
        'platform': platform_name,
        'spider_result': spider_result,
        'validation_result': validation_result,
    }


def create_platform_dag(platform_name: str, platform_config: dict) -> DAG:
    """
    Create a DAG for a specific platform.
    
    Args:
        platform_name: Name of the platform
        platform_config: Configuration dictionary for the platform
        
    Returns:
        Airflow DAG object
    """
    # Default arguments
    default_args = {
        'owner': 'data-team',
        'depends_on_past': False,
        'email_on_failure': True,
        'email_on_retry': False,
        'retries': 3,
        'retry_delay': timedelta(minutes=5),
        'execution_timeout': timedelta(hours=2),
    }
    
    # Parse schedule from config (cron format)
    schedule = platform_config.get('schedule', '0 2 * * *')  # Default: 2 AM daily
    
    # Create DAG
    dag = DAG(
        dag_id=f'scrape_{platform_name}',
        default_args=default_args,
        description=f'Scrape data from {platform_config.get("name", platform_name)}',
        schedule_interval=schedule,
        start_date=days_ago(1),
        catchup=False,
        tags=['scraping', 'biomedical', platform_name],
    )
    
    with dag:
        # Task 1: Run spider
        run_spider_task = PythonOperator(
            task_id=f'run_spider_{platform_name}',
            python_callable=run_spider,
            op_kwargs={'platform_name': platform_name},
            provide_context=True,
        )
        
        # Task 2: Validate data
        validate_task = PythonOperator(
            task_id=f'validate_data_{platform_name}',
            python_callable=validate_data,
            op_kwargs={'platform_name': platform_name},
            provide_context=True,
        )
        
        # Task 3: Export to CSV (using bash for simplicity)
        export_task = BashOperator(
            task_id=f'export_csv_{platform_name}',
            bash_command=f'python -c "from common.pipeline.data_pipeline import DataPipeline; '
                        f'DataPipeline().export_to_csv(\'{platform_name}\')"',
        )
        
        # Task 4: Send notification
        notify_task = PythonOperator(
            task_id=f'notify_{platform_name}',
            python_callable=send_notification,
            op_kwargs={'platform_name': platform_name},
            provide_context=True,
        )
        
        # Define task dependencies
        run_spider_task >> validate_task >> export_task >> notify_task
    
    return dag


# Load configurations and generate DAGs
platform_configs = load_platform_configs()

# Dynamically create DAGs for each platform
for platform_name, platform_config in platform_configs.items():
    # Check if platform is enabled
    if platform_config.get('enabled', True):
        # Create DAG and add to globals (required by Airflow)
        dag_id = f'scrape_{platform_name}'
        globals()[dag_id] = create_platform_dag(platform_name, platform_config)
        
        logging.info(f"Created DAG: {dag_id}")
    else:
        logging.info(f"Skipped disabled platform: {platform_name}")
