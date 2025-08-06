from dagster import job, op, ScheduleDefinition
import subprocess

@op
def scrape_telegram_data():
    # Example: run your Telegram scraper script
    subprocess.run(["python", "scripts/telegram_scraper.py"], check=True)

@op
def load_raw_to_postgres():
    # Loads all Telegram JSONs into raw.telegram_messages
    subprocess.run(["python", "scripts/load_raw_json_to_pg.py"], check=True)

@op
def run_dbt_transformations():
    subprocess.run(["dbt", "seed"], cwd="my_project", check=True)
    subprocess.run(["dbt", "run"], cwd="my_project", check=True)

@op
def run_yolo_enrichment():
    subprocess.run(["python", "scripts/yolo_image_detection.py"], check=True)

@job
def shipping_data_pipeline():
    scrape_telegram_data()
    load_raw_to_postgres()
    run_dbt_transformations()
    run_yolo_enrichment()

# Example schedule: run daily at midnight
shipping_data_schedule = ScheduleDefinition(
    job=shipping_data_pipeline,
    cron_schedule="0 0 * * *",
)
