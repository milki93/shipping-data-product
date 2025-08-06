Shipping Data Product

This project scrapes and collects data from public Telegram channels related to Ethiopian medical businesses. 
It uses Docker for containerization and PostgreSQL for data storage.

Main features:
- Telegram message and image scraping
- Data lake organization by date and channel
- Environment management with Docker and .env files

Setup:
1. Add your Telegram and database credentials to a .env file.
2. Build and run the project with Docker Compose.
3. Run the Telegram scraper script from the scripts/ directory.


## Task 3: Data Enrichment with Object Detection (YOLOv8)

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

For more details, see `scripts/yolo_image_detection.py` and the dbt model in `my_project/models/fct_image_detections.sql`.

See scripts/telegram_scraper.py for the main data collection logic.