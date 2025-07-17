# Staging Models

This directory contains staging models that clean and lightly restructure the raw data from the data lake. Staging models perform tasks like:
- Casting data types
- Renaming columns
- Extracting key fields from JSON

Each raw source should have a corresponding staging model (e.g., stg_telegram_messages.sql). 