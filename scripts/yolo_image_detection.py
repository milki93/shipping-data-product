import os
import json
import csv
from pathlib import Path
from ultralytics import YOLO
from dotenv import load_dotenv

# Load environment variables if needed
load_dotenv()

# Paths
DATA_LAKE_BASE = Path(__file__).parent.parent / 'data' / 'raw' / 'telegram_messages'
OUTPUT_CSV = DATA_LAKE_BASE / 'yolo_detections.csv'
MODEL_NAME = os.getenv('YOLO_MODEL', 'yolov8n.pt')  # Allow override via env
YOLO_CONF = float(os.getenv('YOLO_CONFIDENCE', '0.1'))  # Allow override via env, default 0.1

# Load YOLOv8 model
model = YOLO(MODEL_NAME)

def find_images_and_messages():
    """Yield (message_id, image_path, full_image_path) for each image referenced in message JSON files."""
    for date_dir in DATA_LAKE_BASE.iterdir():
        if not date_dir.is_dir():
            continue
        for channel_dir in date_dir.iterdir():
            if not channel_dir.is_dir():
                continue
            for json_file in channel_dir.glob('*.json'):
                with open(json_file, 'r', encoding='utf-8') as f:
                    try:
                        messages = json.load(f)
                    except Exception as e:
                        print(f"Failed to load {json_file}: {e}")
                        continue
                    for i, msg in enumerate(messages):
                        msg_id = msg.get('id')
                        img_rel_path = msg.get('image_path')
                        if img_rel_path:
                            # Prepend date_dir to the image path
                            img_full_path = (date_dir / img_rel_path).resolve()
                            if i < 5:
                                print(f"DEBUG: msg_id={msg_id}, img_rel_path={img_rel_path}, resolved={img_full_path}, exists={img_full_path.exists()}")
                            if img_full_path.exists():
                                yield msg_id, str(img_rel_path), str(img_full_path)


def run_detection():
    results = []
    total_images = 0
    total_detections = 0
    for msg_id, img_rel_path, img_full_path in find_images_and_messages():
        total_images += 1
        print(f"Detecting objects in {img_rel_path} (message_id={msg_id})...")
        try:
            yolo_results = model(img_full_path, conf=YOLO_CONF)
            boxes = yolo_results[0].boxes
            names = yolo_results[0].names if hasattr(yolo_results[0], 'names') else {}
            if len(boxes) == 0:
                print(f"  No objects detected in {img_rel_path}.")
            for det in boxes:
                cls_id = int(det.cls[0])
                label = names.get(cls_id, str(cls_id))
                results.append({
                    'message_id': msg_id,
                    'image_path': img_rel_path,
                    'detected_object_class': cls_id,
                    'detected_object_label': label,
                    'confidence_score': float(det.conf[0]),
                    'bbox': [float(x) for x in det.xyxy[0].tolist()]
                })
                total_detections += 1
        except Exception as e:
            print(f"Error processing {img_full_path}: {e}")
    print(f"Processed {total_images} images. Total detections: {total_detections}.")
    return results


def save_results_to_csv(results, output_csv):
    if not results:
        print("No detections to save.")
        return
    keys = results[0].keys()
    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(results)
    print(f"Saved detections to {output_csv}")

def copy_csv_to_dbt_seed():
    import shutil
    dbt_seed_path = Path(__file__).parent.parent / 'my_project' / 'seeds' / 'stg_image_detections.csv'
    dbt_seed_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(OUTPUT_CSV, dbt_seed_path)
    print(f"Copied detections to dbt seed: {dbt_seed_path}")

if __name__ == '__main__':
    detections = run_detection()
    save_results_to_csv(detections, OUTPUT_CSV)
    copy_csv_to_dbt_seed()
