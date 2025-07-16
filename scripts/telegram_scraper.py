import os
import json
import logging
from datetime import datetime
from pathlib import Path
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_ID = os.getenv('TELEGRAM_API_ID')
API_HASH = os.getenv('TELEGRAM_API_HASH')
SESSION_NAME = os.getenv('TELEGRAM_SESSION', 'anon')

# Channels to scrape
CHANNELS = [
    'https://t.me/lobelia4cosmetics',
    'https://t.me/tikvahpharma',
    'https://t.me/CheMed123',
    
]

# Data lake base directory
DATA_LAKE_BASE = Path('data/raw/telegram_messages')

# Logging setup
logging.basicConfig(
    filename='scraper.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

async def scrape_channel(client, channel_url):
    try:
        channel = await client.get_entity(channel_url)
        today = datetime.now().strftime('%Y-%m-%d')
        channel_name = channel.username or channel.title.replace(' ', '_')
        out_dir = DATA_LAKE_BASE / today / channel_name
        out_dir.mkdir(parents=True, exist_ok=True)
        messages = []
        async for message in client.iter_messages(channel):
            msg_dict = message.to_dict()
            messages.append(msg_dict)
            # Download images if present
            if message.photo:
                img_path = out_dir / f"{message.id}.jpg"
                await client.download_media(message, file=img_path)
        # Save messages as JSON
        out_file = out_dir / f"{channel_name}.json"
        with open(out_file, 'w', encoding='utf-8') as f:
            json.dump(messages, f, ensure_ascii=False, indent=2)
        logging.info(f"Scraped {len(messages)} messages from {channel_url}")
    except Exception as e:
        logging.error(f"Error scraping {channel_url}: {e}")

async def main():
    async with TelegramClient(SESSION_NAME, API_ID, API_HASH) as client:
        if not await client.is_user_authorized():
            try:
                await client.send_code_request(os.getenv('TELEGRAM_PHONE'))
                await client.sign_in(os.getenv('TELEGRAM_PHONE'), input('Enter the code: '))
            except SessionPasswordNeededError:
                await client.sign_in(password=input('Two-step verification password: '))
        for channel_url in CHANNELS:
            await scrape_channel(client, channel_url)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main()) 