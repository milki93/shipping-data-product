import os
import json
import psycopg2
from glob import glob
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

DB_PARAMS = {
    'dbname': os.getenv('POSTGRES_DB'),
    'user': os.getenv('POSTGRES_USER'),
    'password': os.getenv('POSTGRES_PASSWORD'),
    'host': os.getenv('POSTGRES_HOST', 'db'),  # Use 'db' for Docker Compose
    'port': os.getenv('POSTGRES_PORT', 5432),
}

def create_table(cur):
    cur.execute('''
        CREATE SCHEMA IF NOT EXISTS raw;
        CREATE TABLE IF NOT EXISTS raw.telegram_messages (
            id SERIAL PRIMARY KEY,
            message_json JSONB
        );
    ''')

def load_json_files(cur):
    import glob
    files = glob.glob('data/raw/telegram_messages/**/*.json', recursive=True)
    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            messages = json.load(f)
            for msg in messages:
                cur.execute(
                    "INSERT INTO raw.telegram_messages (message_json) VALUES (%s)",
                    [json.dumps(msg)]
                )

def main():
    conn = psycopg2.connect(**DB_PARAMS)
    cur = conn.cursor()
    create_table(cur)
    load_json_files(cur)
    conn.commit()
    cur.close()
    conn.close()
    print('Loaded raw JSON files into raw.telegram_messages')

if __name__ == '__main__':
    main() 