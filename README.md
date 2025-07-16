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

See scripts/telegram_scraper.py for the main data collection logic.