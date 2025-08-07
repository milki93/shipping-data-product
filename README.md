# 🚢 Shipping Data Product

This project scrapes and collects data from public Telegram channels related to Ethiopian medical businesses.  
It uses Docker for containerization and PostgreSQL for data storage.

Main features:
- Telegram message and image scraping
- Data lake organization by date and channel
- Environment management with Docker and `.env` files

---

## Data Scraping and Collection (Extract & Load)

This task collects raw message and image data from selected Ethiopian medical Telegram channels using the **Telethon** library.

### 🔍 What it Does

- Scrapes messages and associated images from public channels.
- Organizes raw data into a data lake directory


- Logs scraping status, success, and errors.

### How to Run

```bash
python scripts/telegram_scraper.py
```

### Features

- Skips already scraped dates and channels using logs

- Handles API rate limits and retries automatically

- Stores image metadata for further analysis

## Data Enrichment with Object Detection (YOLOv8)

This task enriches Telegram message data with object detection results using a pre-trained YOLOv8 model. Detected objects in images are integrated into the analytics warehouse via dbt.

### 1. Environment Setup

- Ensure Python 3.8+ and pip are installed.
- Install dependencies:

```sh
pip install -r requirements.txt
```

- Activate your virtual environment if using one:
```sh
source venv/bin/activate
```

### 2. Run YOLOv8 Image Detection

From the project root:
```sh
python scripts/yolo_image_detection.py
```
This will:
- Scan Telegram message JSONs for images
- Run YOLOv8 object detection on each image
- Save detection results to a CSV
- Copy the CSV to `my_project/seeds/stg_image_detections.csv` for dbt integration

--- 

## Data Modeling and Transformation (Transform with dbt)

This task uses **dbt (Data Build Tool)** to transform the raw Telegram data into clean, structured tables for analysis.

### What it does:
- Loads raw JSON data into PostgreSQL.
- Transforms the data using dbt models into a **star schema** with:
  - `dim_channels` (channel info)
  - `dim_dates` (date info)
  - `fct_messages` (core message data)
- Ensures data quality with basic tests (e.g., `not_null`, `unique`).


### 3. Load Detection Results into the Data Warehouse (dbt)

From the `my_project` directory:
```sh
cd my_project
# Load the detection CSV as a seed table
source ../venv/bin/activate  # if using a venv

dbt seed --select stg_image_detections
# Build the fact table with detections linked to messages

dbt run --select fct_image_detections
```

- The `stg_image_detections` seed table will be created from the CSV.
- The `fct_image_detections` model will join detections to the core messages model using `message_id`.

### 4. Testing
- Inspect `my_project/seeds/stg_image_detections.csv` to verify detection results.
- Use your database or dbt to query `fct_image_detections` and confirm detections are present and joined to messages.

### Troubleshooting
- Ensure the CSV is in the `seeds/` directory, not `data/`.
- If `dbt` is not found, activate your Python environment.
- Check logs for any errors during detection or dbt runs.

---

## Analytical API with FastAPI

This API exposes analytical endpoints over your dbt models using FastAPI.

### API Structure

- All FastAPI code is in the `api/` directory:
    - `main.py` – FastAPI entrypoint
    - `database.py` – Loads DB credentials from `.env` using python-dotenv and provides psycopg2 connection
    - `schemas.py` – Pydantic response schemas
    - `crud.py` – Query logic for endpoints (uses raw psycopg2 SQL)

### How to Run

1. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```
2. Ensure your `.env` file is in the project root, with correct PostgreSQL credentials
3. Start the API from the project root so `.env` is loaded:
    ```sh
    uvicorn api.main:app --reload
    ```

### Endpoints

- `GET /api/reports/top-products?limit=10` – Most frequently mentioned products
- `GET /api/channels/{channel_name}/activity` – Posting activity for a channel
- `GET /api/search/messages?query=paracetamol` – Search for messages by keyword


---

## Troubleshooting

### API returns 500 or "relation does not exist"
- Confirm you ran `dbt seed` and `dbt run` for your models.
- Make sure both dbt and FastAPI use the same `.env` and database credentials.
- Use `psql` or DBeaver to check that views like `fct_image_detections` and `fct_messages` exist in the correct schema (usually `public`).
- If models are missing, check your dbt `profiles.yml` and `.env` for mismatches.
- Restart the API server after running dbt to refresh connections.
- If using a virtual environment, ensure it is activated before running dbt or FastAPI.

See scripts/telegram_scraper.py for the main data collection logic.

---

## Pipeline Orchestration with Dagster

To make your workflow robust, observable, and schedulable, this project uses [Dagster](https://dagster.io/) for orchestration.

### 1. Install Dagster

Install the required packages:
```sh
pip install -r requirements.txt
```

### 2. Pipeline Structure
- The Dagster pipeline is defined in `orchestration/pipeline.py`.
- **Current workflow:**
  - `scrape_telegram_data`: **Inactive by default** (data already present). To reactivate, uncomment the subprocess line in the op.
  - `load_raw_to_postgres`: Loads all Telegram JSON files into Postgres using `scripts/load_raw_json_to_pg.py`.
  - `run_dbt_transformations`: Runs `dbt seed` and `dbt run` to build analytics models in `my_project`.
  - `run_yolo_enrichment`: Runs YOLOv8 image detection and prepares data for dbt.
- These steps are combined into a single job: `shipping_data_pipeline`.
- A daily schedule is provided (`shipping_data_schedule`).

### 3. Launch the Dagster UI

From the project root, activate your virtual environment and run:
```sh
source venv/bin/activate
pip install -r requirements.txt  # ensure all dependencies

dagster dev -f orchestration/pipeline.py
```
- The UI will be available at http://localhost:3000
- You can run, monitor, and schedule your pipeline from the UI.

**Troubleshooting:**
- If the UI does not open, check for errors in the terminal and ensure all requirements are installed in your active virtual environment.

### 4. Customizing Ops
- Edit `orchestration/pipeline.py` to customize or expand pipeline steps as needed for your project.

### 5. Scheduling
- The pipeline is scheduled to run daily at midnight by default. You can activate or modify this schedule in the Dagster UI.

### Example Directory Structure
```
shipping-data-product/
├── orchestration/
│   └── pipeline.py
├── scripts/
│   └── yolo_image_detection.py
│   └── telegram_scraper.py
│   └── load_raw_json_to_pg.py
├── my_project/
│   └── ...
├── api/
│   └── ...
├── requirements.txt
├── README.md
```

---
